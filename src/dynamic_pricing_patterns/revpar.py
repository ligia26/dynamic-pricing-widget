from __future__ import annotations
import numpy as np
import pandas as pd
from .data import enrich_bookings, sellable_rooms


def monthly_room_dynamics(bookings, rooms, conv, as_of):
    """Auditable year x month x room dynamics. Occupancy denominator is sellable room inventory x calendar days."""
    b=enrich_bookings(bookings)
    b=b[(b['status'].eq('CONFIRMED')) & (b['checkin_date']<=as_of)].copy()
    room_dim=sellable_rooms(rooms)[['id','name','quantity']].rename(columns={'id':'room_id','name':'room_name_dim','quantity':'rooms_available'})
    b=b.merge(room_dim[['room_id','rooms_available']],on='room_id',how='inner')
    keys=['stay_year','stay_month_num','season','room_id','room_name','rooms_available']
    g=b.groupby(keys,dropna=False).agg(
        bookings=('booking_code','nunique'), room_nights=('room_nights','sum'), revenue=('total_stay_amount','sum'),
        guests=('guests_number','sum'), avg_los=('room_nights','mean'), avg_lead_days=('lead_time_days','mean'),
        adr_booking_mean=('adr','mean')
    ).reset_index()
    g['days_in_month']=pd.to_datetime(dict(year=g.stay_year,month=g.stay_month_num,day=1)).dt.days_in_month
    g['available_room_nights']=g['rooms_available']*g['days_in_month']
    g['occupancy_pct']=100*g['room_nights']/g['available_room_nights'].replace(0,np.nan)
    g['realized_adr']=g['revenue']/g['room_nights'].replace(0,np.nan)
    g['revpar']=g['revenue']/g['available_room_nights'].replace(0,np.nan)
    # Aggregate directional conversion across booking windows to month x room.
    if not conv.empty:
        cv=(conv.groupby(['stay_year','stay_month_num','season','room_name'],dropna=False).agg(
            quoted_requests=('quoted_requests','sum'), same_room_converted=('same_room_converted','sum')
        ).reset_index())
        cv['conversion_pct']=100*cv['same_room_converted']/cv['quoted_requests'].replace(0,np.nan)
        g=g.merge(cv[['stay_year','stay_month_num','season','room_name','quoted_requests','conversion_pct']],
                  on=['stay_year','stay_month_num','season','room_name'],how='left')
    return g.sort_values(['room_name','stay_month_num','stay_year'])


def yoy_dynamics(monthly):
    x=monthly.copy().sort_values(['room_name','stay_month_num','stay_year'])
    grp=x.groupby(['room_name','stay_month_num'],dropna=False)
    for col in ['realized_adr','occupancy_pct','revpar','conversion_pct','room_nights','revenue','avg_los']:
        prev=grp[col].shift(1)
        x[f'prev_{col}']=prev
        if col in ['occupancy_pct','conversion_pct']:
            x[f'{col}_yoy_pp']=x[col]-prev
        else:
            x[f'{col}_yoy_pct']=100*(x[col]-prev)/prev.replace(0,np.nan)
    return x


def classify_regime(row,cfg):
    occ=row['occupancy_pct']
    if pd.isna(occ): return 'INSUFFICIENT_EVIDENCE'
    if occ >= cfg['high_occupancy_pct']: return 'PRICE_POWER'
    if occ <= cfg['low_occupancy_pct']: return 'VOLUME_OPPORTUNITY'
    return 'BALANCED'


def _elasticity_from_history(group,cfg):
    """Estimate a conservative local occupancy response to price from year-over-year observations.
    Returns elasticity e where pct occupancy change ~= -e * pct price change. Falls back to configurable priors.
    This is an observational proxy, not causal elasticity.
    """
    vals=[]
    g=group.sort_values('stay_year')
    for _,r in g.iterrows():
        dp=r.get('realized_adr_yoy_pct',np.nan)
        prev_occ=r.get('prev_occupancy_pct',np.nan)
        occ=r.get('occupancy_pct',np.nan)
        if pd.notna(dp) and abs(dp)>=cfg['min_price_move_for_elasticity_pct'] and pd.notna(prev_occ) and prev_occ>0:
            dq=100*(occ-prev_occ)/prev_occ
            e=-dq/dp
            if np.isfinite(e) and e>=0:
                vals.append(float(np.clip(e,0,cfg['max_elasticity'])))
    if len(vals)>=cfg['min_elasticity_observations']:
        return float(np.median(vals)),len(vals),'OBSERVED'
    med=float(group['occupancy_pct'].median()) if len(group) else 0
    prior=cfg['low_season_elasticity_prior'] if med<=cfg['low_occupancy_pct'] else cfg['high_season_elasticity_prior']
    return float(prior),len(vals),'PRIOR'


def optimize_revpar(monthly_yoy,cfg):
    rows=[]
    steps=[float(v) for v in cfg['price_steps_pct']]
    for (room,month),hist in monthly_yoy.groupby(['room_name','stay_month_num'],dropna=False):
        elasticity,nobs,source=_elasticity_from_history(hist,cfg)
        for _,r in hist.iterrows():
            regime=classify_regime(r,cfg)
            base_adr=float(r['realized_adr']) if pd.notna(r['realized_adr']) else np.nan
            base_occ=float(r['occupancy_pct']) if pd.notna(r['occupancy_pct']) else np.nan
            avail=float(r['available_room_nights'])
            if not np.isfinite(base_adr) or not np.isfinite(base_occ): continue
            candidates=[]
            for step in steps:
                # elasticity operates on relative occupancy; capacity caps the upside.
                occ=max(0.0,min(100.0,base_occ*(1-elasticity*(step/100.0))))
                adr=base_adr*(1+step/100.0)
                revpar=adr*occ/100.0
                revenue=revpar*avail
                candidates.append((step,adr,occ,revpar,revenue))
            # High season: price-up only, preserving occupancy within tolerance. Low season: allow discounts to stimulate volume.
            if regime=='PRICE_POWER':
                valid=[c for c in candidates if c[0]>=0 and c[2]>=base_occ-cfg['high_season_max_occupancy_loss_pp']]
            elif regime=='VOLUME_OPPORTUNITY':
                valid=[c for c in candidates if c[0]<=0 or c[0]==0]
            else:
                valid=candidates
            best=max(valid,key=lambda z:z[3]) if valid else min(candidates,key=lambda z:abs(z[0]))
            step,adr,occ,revpar,revenue=best
            impact=revenue-float(r['revenue'])
            # Never recommend a negative economic move.
            if impact<=cfg['min_incremental_revenue_eur'] or abs(step)<1e-9:
                step=0.0; adr=base_adr; occ=base_occ; revpar=float(r['revpar']); revenue=float(r['revenue']); impact=0.0
                action='HOLD'
            else:
                action='PRICE_DOWN' if step<0 else 'PRICE_UP'
            evidence='HIGH' if source=='OBSERVED' and nobs>=2 else ('MEDIUM' if source=='OBSERVED' else 'LOW')
            rows.append({
                'stay_year':int(r['stay_year']),'stay_month_num':int(month),'season':r['season'],'room_name':room,
                'regime':regime,'strategy':action,'current_adr':round(base_adr,2),'recommended_price_change_pct':round(step,2),
                'recommended_adr':round(adr,2),'current_occupancy_pct':round(base_occ,2),'expected_occupancy_pct':round(occ,2),
                'current_revpar':round(float(r['revpar']),2),'optimized_revpar':round(revpar,2),
                'revpar_change_pct':round(100*(revpar-float(r['revpar']))/float(r['revpar']),2) if r['revpar'] else np.nan,
                'actual_revenue':round(float(r['revenue']),2),'optimized_revenue':round(revenue,2),'incremental_revenue_eur':round(impact,2),
                'room_nights':round(float(r['room_nights']),2),'available_room_nights':round(avail,2),
                'conversion_pct':round(float(r['conversion_pct']),2) if pd.notna(r.get('conversion_pct')) else np.nan,
                'avg_los':round(float(r['avg_los']),2) if pd.notna(r['avg_los']) else np.nan,
                'elasticity_proxy':round(elasticity,3),'elasticity_source':source,'elasticity_observations':int(nobs),'confidence':evidence,
                'reason':f"{regime}: tested price grid and selected {step:+.0f}% because it maximizes modeled RevPAR ({r['revpar']:.2f} -> {revpar:.2f}) under the estimated price-volume response."
            })
    return pd.DataFrame(rows).sort_values('incremental_revenue_eur',ascending=False)


def yearly_opportunity(recs):
    if recs.empty: return pd.DataFrame()
    return recs.groupby(['stay_year','strategy'],dropna=False).agg(
        contexts=('room_name','size'), actual_revenue=('actual_revenue','sum'), optimized_revenue=('optimized_revenue','sum'),
        incremental_revenue_eur=('incremental_revenue_eur','sum')
    ).reset_index().sort_values(['stay_year','incremental_revenue_eur'],ascending=[True,False])
