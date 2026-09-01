from __future__ import annotations
import numpy as np
import pandas as pd
from .data import enrich_bookings

BOARD_RANK={
    # Commercial board ladder only. Ownership/residence arrangements are intentionally excluded.
    'No Board':0,'Only Bed':0,'Solo Pernottamento':0,
    'Bed & Breakfast':1,'Mezza Pensione':2,'Mezza Pensione Pranzo':2,'Pensione Completa':3,
}


def treatment_context_dynamics(bookings, as_of):
    """Auditable year x month x room x treatment economics.
    ADR is TOTAL-STAY ADR, not a separately observed treatment add-on price.
    """
    b=enrich_bookings(bookings)
    b=b[(b['status'].eq('CONFIRMED'))&(b['checkin_date']<=as_of)].copy()
    keys=['stay_year','stay_month_num','season','room_name','arrangement_name']
    g=b.groupby(keys,dropna=False).agg(
        bookings=('booking_code','nunique'),room_nights=('room_nights','sum'),
        revenue=('total_stay_amount','sum'),guests=('guests_number','sum'),
        avg_los=('room_nights','mean'),avg_lead_days=('lead_time_days','mean')
    ).reset_index()
    g['realized_total_adr']=g['revenue']/g['room_nights'].replace(0,np.nan)
    denom=g.groupby(['stay_year','stay_month_num','room_name'])['bookings'].transform('sum')
    g['treatment_mix_pct']=100*g['bookings']/denom.replace(0,np.nan)
    return g.sort_values(['room_name','arrangement_name','stay_month_num','stay_year'])


def treatment_price_recommendations(dynamics,cfg):
    """Same-treatment price-resilience candidates at room x month granularity.
    We deliberately call the price TOTAL PACKAGE ADR because source data does not isolate treatment add-on price.
    """
    x=dynamics.copy().sort_values(['room_name','arrangement_name','stay_month_num','stay_year'])
    grp=x.groupby(['room_name','arrangement_name','stay_month_num'],dropna=False)
    x['prev_total_adr']=grp['realized_total_adr'].shift(1)
    x['prev_room_nights']=grp['room_nights'].shift(1)
    x['prev_bookings']=grp['bookings'].shift(1)
    x['total_adr_yoy_pct']=100*(x['realized_total_adr']-x['prev_total_adr'])/x['prev_total_adr'].replace(0,np.nan)
    x['volume_yoy_pct']=100*(x['room_nights']-x['prev_room_nights'])/x['prev_room_nights'].replace(0,np.nan)
    x['price_resilient']=(
        (x['prev_bookings']>=cfg.get('treatment_min_prior_bookings',10)) &
        (x['bookings']>=cfg.get('treatment_min_current_bookings',10)) &
        (x['total_adr_yoy_pct']>=cfg['treatment_min_price_increase_pct']) &
        (x['volume_yoy_pct']>=-cfg['treatment_max_volume_decline_pct'])
    )
    x['recommended_price_change_pct']=np.where(x['price_resilient'],cfg['treatment_test_uplift_pct'],0.0)
    x['strategy']=np.where(x['price_resilient'],'PACKAGE_PRICE_UP','HOLD')
    x['recommended_total_adr']=x['realized_total_adr']*(1+x['recommended_price_change_pct']/100)
    x['incremental_revenue_eur']=np.where(
        x['price_resilient'],x['revenue']*x['recommended_price_change_pct']/100,0.0
    )
    x['confidence']=np.select([
        x['price_resilient']&(x['bookings']>=30)&(x['prev_bookings']>=30),
        x['price_resilient']
    ],['HIGH','MEDIUM'],default='LOW')
    x['action_text']=np.where(
        x['price_resilient'],
        x['room_name'].astype(str)+' · '+x['arrangement_name'].astype(str)+' · month '+x['stay_month_num'].astype(str)+
        ': test TOTAL PACKAGE ADR '+x['recommended_price_change_pct'].map(lambda v:f'{v:+.0f}%'),
        'HOLD'
    )
    x['note']='TOTAL PACKAGE ADR signal. Source does not isolate the treatment add-on price, so this must not be described as a +X% treatment-component price.'
    return x.sort_values('incremental_revenue_eur',ascending=False)


def treatment_promotion_candidates(dynamics,cfg):
    """Evidence-backed bundle/upsell candidates, not causal transition claims.

    For a room-month-year, compare lower-board and higher-board observed packages.
    A candidate exists only when the higher board has meaningful observed adoption.
    `package_adr_premium_eur` is the observed TOTAL ADR difference, not the treatment's standalone price.
    """
    rows=[]
    min_high=int(cfg.get('upsell_min_higher_treatment_bookings',10))
    min_share=float(cfg.get('upsell_min_higher_treatment_share_pct',10))
    target=float(cfg.get('upsell_target_rate_pct',10))/100.0
    for (yr,mo,season,room),g in dynamics.groupby(['stay_year','stay_month_num','season','room_name'],dropna=False):
        gg=g.copy()
        gg['rank']=gg['arrangement_name'].map(BOARD_RANK)
        gg=gg[gg['rank'].notna()].sort_values('rank')
        if len(gg)<2: continue
        for _,low in gg.iterrows():
            higher=gg[gg['rank']>low['rank']]
            if higher.empty: continue
            # nearest higher board with enough real adoption; prefer the most-booked qualifying option.
            higher=higher[(higher['bookings']>=min_high)&(higher['treatment_mix_pct']>=min_share)]
            if higher.empty: continue
            high=higher.sort_values(['rank','bookings'],ascending=[True,False]).iloc[0]
            premium=float(high['realized_total_adr']-low['realized_total_adr'])
            if not np.isfinite(premium) or premium<=0: continue
            eligible=float(low['bookings'])
            expected_upgrades=eligible*target
            proxy=expected_upgrades*premium*float(low['avg_los'] if pd.notna(low['avg_los']) else 1.0)
            confidence='HIGH' if high['bookings']>=30 and low['bookings']>=30 else 'MEDIUM'
            rows.append({
                'stay_year':int(yr),'stay_month_num':int(mo),'season':season,'room_name':room,
                'from_treatment':low['arrangement_name'],'to_treatment':high['arrangement_name'],
                'strategy':'PROMOTE_UPSELL','eligible_lower_treatment_bookings':int(low['bookings']),
                'observed_higher_treatment_bookings':int(high['bookings']),
                'observed_higher_treatment_share_pct':round(float(high['treatment_mix_pct']),2),
                'lower_total_adr':round(float(low['realized_total_adr']),2),
                'higher_total_adr':round(float(high['realized_total_adr']),2),
                'package_adr_premium_eur':round(premium,2),'test_upgrade_rate_pct':round(target*100,2),
                'expected_test_upgrades':round(expected_upgrades,2),
                'economic_value_proxy_eur':round(proxy,2),'confidence':confidence,
                'action_text':f"{room} · month {int(mo)}: promote {low['arrangement_name']} → {high['arrangement_name']} to a controlled test cohort ({target*100:.0f}% target).",
                'note':'EVIDENCE-BASED TEST CANDIDATE ONLY. No booking-level treatment transition is observed. Economic value uses total-package ADR premium as a proxy and is NON-ADDITIVE.'
            })
    return pd.DataFrame(rows).sort_values('economic_value_proxy_eur',ascending=False) if rows else pd.DataFrame()


def upsell_evidence(bookings, as_of):
    """Backward-compatible descriptive treatment-mix output."""
    return treatment_context_dynamics(bookings,as_of)
