from __future__ import annotations
import re
import numpy as np
import pandas as pd

from .decision_timing import (
    _timing_config, _norm, _request_count, _historical_state,
    _conversion_at_date, _booked_room_nights_at_date,
    _available_room_nights, _safe_ratio, _score, _absolute_support
)

PRICE_TYPES={"PRICE_UP","PRICE_DOWN","PACKAGE_PRICE_UP"}

def _parse_pct(action):
    """Return signed target % from strings such as '+10%' or '-25%'."""
    if not isinstance(action,str):
        return np.nan
    m=re.search(r'([+-]\s*\d+(?:\.\d+)?)\s*%', action)
    if not m:
        return np.nan
    return float(m.group(1).replace(" ",""))

def _stage_step(target_pct, score, lead):
    """
    Convert evidence strength into a progressive move.
    Far from arrival, start smaller; closer/stronger signals can move faster.
    """
    sign=1 if target_pct>0 else -1
    mag=abs(target_pct)
    if lead > 120:
        base=5.0
    elif lead > 60:
        base=5.0 if score < 0.45 else 10.0
    else:
        base=10.0 if score < 0.55 else 15.0
    return sign*min(base,mag)

def build_pricing_trajectory(actions, bookings, requests, quotes, rooms, cfg):
    """
    Reconstruct progressive historical pricing paths.

    Unlike the one-date timing layer, this evaluates the state repeatedly and
    can issue multiple incremental price moves toward the retrospective optimum.
    It only uses information available on each historical evaluation date.
    """
    tc=_timing_config(cfg)
    b=bookings.copy(); r=requests.copy(); q=quotes.copy()
    for x in (b,r):
        x["stay_year"]=x.checkin_date.dt.year
        x["stay_month_num"]=x.checkin_date.dt.month
    for x in (b,r,q):
        x["creation_datetime"]=_norm(x.creation_datetime)
    b["cancellation_datetime"]=_norm(b.cancellation_datetime)

    rows=[]
    for action_id,(_,a) in enumerate(actions.iterrows(), start=1):
        typ=a.action_type
        if typ not in PRICE_TYPES:
            continue
        target_pct=_parse_pct(str(a.action))
        if pd.isna(target_pct) or target_pct==0:
            continue

        year=int(a.stay_year); month=int(a.stay_month_num)
        room=a.room_name
        treatment=str(a.treatment) if pd.notna(a.treatment) and str(a.treatment).strip() else ""
        start=pd.Timestamp(year,month,1)
        cumulative=0.0
        last_move=None
        step_no=0

        # Evaluate from farthest lead time toward arrival.
        for lead in range(tc["max_lead_days"],tc["min_lead_days"]-1,-tc["evaluation_step_days"]):
            d=start-pd.Timedelta(days=lead)
            rc=_request_count(r,q,room,treatment,year,month,d)
            hrc,hcr,hocc=_historical_state(r,q,b,rooms,room,treatment,year,month,lead)
            cr,conv_n,conv_d=_conversion_at_date(r,q,b,room,treatment,year,month,d)
            occ=_booked_room_nights_at_date(b,room,year,month,d)/max(_available_room_nights(rooms,room,year,month),1)*100
            has_hist=pd.notna(hrc) and hrc>=tc["min_historical_requests"]
            req_idx=_safe_ratio(rc,hrc) if has_hist else np.nan
            cr_delta=cr-hcr if pd.notna(cr) and pd.notna(hcr) else np.nan
            score=_score(typ,req_idx,cr_delta,occ,hocc,lead,cfg)
            hist_support=has_hist and score>=tc["score_threshold"]
            abs_support=_absolute_support(typ,occ,cr,rc,tc) and score>=tc["absolute_score_threshold"]
            supported=hist_support or abs_support

            # Require persistence: confirm the next evaluation point also supports direction.
            if not supported:
                continue
            if last_move is not None and (d-last_move).days < 14:
                continue
            remaining=target_pct-cumulative
            if abs(remaining) < 0.01:
                break
            proposed=_stage_step(target_pct,score,lead)
            if abs(proposed)>abs(remaining):
                proposed=remaining

            # Very early actions are deliberately capped to 5%.
            if lead>120:
                proposed=np.sign(proposed)*min(abs(proposed),5.0)

            step_no+=1
            cumulative+=proposed
            last_move=d
            confidence="HIGH" if score>=tc["high_confidence_score"] else "MEDIUM"
            rows.append({
                "source_action_id":action_id,
                "decision_date":d.date().isoformat(),
                "stay_year":year,
                "stay_month_num":month,
                "room_name":room,
                "treatment":treatment or np.nan,
                "action_type":typ,
                "trajectory_step":step_no,
                "price_change_this_step_pct":round(proposed,2),
                "cumulative_price_change_pct":round(cumulative,2),
                "retrospective_target_change_pct":round(target_pct,2),
                "lead_days_to_stay_month":lead,
                "requests_to_date":rc,
                "historical_requests_same_lead":round(hrc,1) if pd.notna(hrc) else np.nan,
                "request_pace_index":round(req_idx,3) if pd.notna(req_idx) else np.nan,
                "conversion_to_date_pct":round(cr,2) if pd.notna(cr) else np.nan,
                "historical_conversion_same_lead_pct":round(hcr,2) if pd.notna(hcr) else np.nan,
                "conversion_delta_pp":round(cr_delta,2) if pd.notna(cr_delta) else np.nan,
                "occupancy_on_books_pct":round(occ,2),
                "historical_occupancy_same_lead_pct":round(hocc,2) if pd.notna(hocc) else np.nan,
                "timing_score":round(score,3),
                "timing_confidence":confidence,
                "economic_value_eur_final_target":a.get("economic_value_eur",np.nan),
                "decision_reason":(
                    f"Progressive {typ} move: evidence supports the target direction with "
                    f"{lead} days to stay month. Move {proposed:+.0f}% now; cumulative "
                    f"{cumulative:+.0f}% toward retrospective target {target_pct:+.0f}%."
                ),
            })

    cols=[
        "source_action_id","decision_date","stay_year","stay_month_num","room_name","treatment",
        "action_type","trajectory_step","price_change_this_step_pct","cumulative_price_change_pct",
        "retrospective_target_change_pct","lead_days_to_stay_month","requests_to_date",
        "historical_requests_same_lead","request_pace_index","conversion_to_date_pct",
        "historical_conversion_same_lead_pct","conversion_delta_pp","occupancy_on_books_pct",
        "historical_occupancy_same_lead_pct","timing_score","timing_confidence",
        "economic_value_eur_final_target","decision_reason"
    ]
    return pd.DataFrame(rows,columns=cols)
