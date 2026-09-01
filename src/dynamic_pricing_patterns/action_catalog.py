from __future__ import annotations
import pandas as pd

def build_action_catalog(room_recs, package_recs, promotions):
    rows=[]
    for _,r in room_recs[room_recs['strategy'].ne('HOLD')].iterrows():
        rows.append({
            'stay_year':r['stay_year'],'stay_month_num':r['stay_month_num'],'room_name':r['room_name'],
            'treatment':'','action_type':r['strategy'],
            'action':f"Change ROOM ADR {r['recommended_price_change_pct']:+.0f}% ({r['current_adr']:.2f} → {r['recommended_adr']:.2f})",
            'current_occupancy_pct':r['current_occupancy_pct'],'expected_occupancy_pct':r['expected_occupancy_pct'],
            'current_revpar':r['current_revpar'],'optimized_revpar':r['optimized_revpar'],
            'economic_value_eur':r['incremental_revenue_eur'],'economic_value_type':'MODELED_REVENUE',
            'confidence':r['confidence'],'evidence':r['elasticity_source'],
            'why':r['reason']
        })
    for _,r in package_recs[package_recs['strategy'].eq('PACKAGE_PRICE_UP')].iterrows():
        rows.append({
            'stay_year':r['stay_year'],'stay_month_num':r['stay_month_num'],'room_name':r['room_name'],
            'treatment':r['arrangement_name'],'action_type':'PACKAGE_PRICE_UP',
            'action':f"Test TOTAL PACKAGE ADR {r['recommended_price_change_pct']:+.0f}% for {r['arrangement_name']}",
            'current_occupancy_pct':None,'expected_occupancy_pct':None,'current_revpar':None,'optimized_revpar':None,
            'economic_value_eur':r['incremental_revenue_eur'],'economic_value_type':'NON_ADDITIVE_PACKAGE_SIMULATION',
            'confidence':r['confidence'],'evidence':'OBSERVED_YOY_PRICE_AND_VOLUME',
            'why':f"Total ADR YoY {r['total_adr_yoy_pct']:+.1f}% while room-night volume YoY {r['volume_yoy_pct']:+.1f}%."
        })
    if promotions is not None and not promotions.empty:
        for _,r in promotions.iterrows():
            rows.append({
                'stay_year':r['stay_year'],'stay_month_num':r['stay_month_num'],'room_name':r['room_name'],
                'treatment':f"{r['from_treatment']} → {r['to_treatment']}",'action_type':'PROMOTE_UPSELL',
                'action':r['action_text'],'current_occupancy_pct':None,'expected_occupancy_pct':None,
                'current_revpar':None,'optimized_revpar':None,'economic_value_eur':r['economic_value_proxy_eur'],
                'economic_value_type':'NON_ADDITIVE_TEST_PROXY','confidence':r['confidence'],
                'evidence':'OBSERVED_TREATMENT_MIX',
                'why':f"Higher board already represents {r['observed_higher_treatment_share_pct']:.1f}% of bookings in this room-month; observed total-ADR premium €{r['package_adr_premium_eur']:.2f}."
            })
    return pd.DataFrame(rows).sort_values(['stay_year','stay_month_num','economic_value_eur'],ascending=[False,True,False])
