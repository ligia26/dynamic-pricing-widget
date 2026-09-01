from __future__ import annotations
import re
import numpy as np
import pandas as pd

PRICE_ACTIONS={"PRICE_UP","PRICE_DOWN","PACKAGE_PRICE_UP"}




# v0.9 timing philosophy:
# - widen coverage using multiple independent evidence routes;
# - never assign a date from weak request volume alone;
# - downgrade confidence when the trigger relies on absolute-state evidence;
# - keep retrospective economic action unchanged.

DEFAULT_TIMING_CONFIG = {
    "max_lead_days": 180,
    "min_lead_days": 14,
    "evaluation_step_days": 7,
    "sustain_days": 7,

    "min_current_requests": 8,
    "min_historical_requests": 5,
    "high_confidence_historical_requests": 25,
    "high_confidence_current_requests": 35,

    "request_index_scale": 0.30,
    "conversion_delta_scale_pp": 12.0,
    "occupancy_delta_scale_pp": 15.0,
    "neutral_occupancy_pct": 55.0,
    "occupancy_level_scale_pp": 35.0,
    "lead_time_bonus": 0.08,

    "score_threshold": 0.24,
    "absolute_score_threshold": 0.14,
    "high_confidence_score": 0.52,

    "weights": {
        "request_pace": 0.40,
        "conversion": 0.25,
        "occupancy_pace": 0.20,
        "occupancy_level": 0.15,
    },

    "absolute_price_up_occupancy_pct": 65.0,
    "absolute_price_up_conversion_pct": 35.0,
    "absolute_price_down_occupancy_pct": 48.0,

    "upsell_min_source_requests": 4,
    "upsell_min_target_requests": 4,
    "upsell_min_target_request_share_pct": 8.0,
    "upsell_min_target_conversion_pct": 5.0,
    "upsell_target_share_scale_pct": 35.0,
    "upsell_target_request_scale": 30.0,
    "upsell_conversion_scale_pct": 35.0,
    "upsell_high_confidence_score": 0.65,

    # v0.9 coverage expansion: allow moderate but corroborated signals
    "moderate_request_up_ratio": 1.12,
    "moderate_request_down_ratio": 0.90,
    "moderate_conversion_delta_pp": 3.0,
    "moderate_occupancy_delta_pp": 6.0,
    "min_corroborating_signals": 2,
    "very_early_lead_days": 120,
    "very_early_score_multiplier": 1.35,

    # v1.1 timing precision fallback:
    # EXACT if the normal sustained trigger is found.
    # Otherwise infer MONTH / WINDOW from weaker but persistent directional evidence.
    "month_inference_score_threshold": 0.10,
    "month_inference_min_evaluations": 2,
    "month_inference_min_signal_count": 2,
    "window_inference_score_threshold": 0.06,
    "upsell_month_score_threshold": 0.28,
    "upsell_window_score_threshold": 0.20,
}

def _timing_config(cfg):
    """
    Backward-compatible timing configuration.

    v0.8 introduced additional timing parameters. Older repositories may have
    a partial decision_timing section, so merge user settings over complete
    internal defaults instead of indexing missing keys directly.
    """
    merged = DEFAULT_TIMING_CONFIG.copy()

    # Deep-copy the nested weights so user overrides don't mutate defaults.
    merged["weights"] = DEFAULT_TIMING_CONFIG["weights"].copy()

    user = (cfg or {}).get("decision_timing", {}) or {}
    for key, value in user.items():
        if key == "weights" and isinstance(value, dict):
            merged["weights"].update(value)
        else:
            merged[key] = value
    return merged


def _norm(s): return pd.to_datetime(s,errors="coerce").dt.normalize()
def _prior_mean(values):
    vals=[v for v in values if pd.notna(v)]
    return float(np.mean(vals)) if vals else np.nan
def _safe_ratio(a,b): return float(a/b) if pd.notna(b) and b>0 else np.nan

def _conversion_at_date(req, quotes, bookings, room, treatment, stay_year, stay_month, decision_date):
    q=quotes[(quotes.room_name==room)&(quotes.creation_datetime<=decision_date)].copy()
    if treatment: q=q[q.arrangement_name==treatment]
    ids=set(q.request_code.dropna().astype(str))
    rr=req[(req.stay_year==stay_year)&(req.stay_month_num==stay_month)&(req.creation_datetime<=decision_date)].copy()
    rr=rr[rr.request_code.astype(str).isin(ids)]
    if rr.empty: return np.nan,0,0
    bb=bookings[(bookings.stay_year==stay_year)&(bookings.stay_month_num==stay_month)&(bookings.creation_datetime<=decision_date)&(bookings.is_canceled.eq(0))]
    bb=bb[bb.room_name==room]
    if treatment: bb=bb[bb.arrangement_name==treatment]
    converted=set(bb.customer_code.dropna().astype(str))
    denom=rr.customer_code.dropna().astype(str).nunique()
    num=rr[rr.customer_code.astype(str).isin(converted)].customer_code.astype(str).nunique()
    return (100.0*num/denom if denom else np.nan),num,denom

def _booked_room_nights_at_date(bookings, room, stay_year, stay_month, decision_date):
    x=bookings[(bookings.room_name==room)&(bookings.stay_year==stay_year)&(bookings.stay_month_num==stay_month)&
               (bookings.creation_datetime<=decision_date)&(bookings.is_canceled.eq(0))].copy()
    if 'cancellation_datetime' in x:
        x=x[x.cancellation_datetime.isna() | (x.cancellation_datetime>decision_date)]
    return float(pd.to_numeric(x.nights,errors='coerce').fillna(0).sum())

def _available_room_nights(rooms, room, stay_year, stay_month):
    qty=pd.to_numeric(rooms.loc[rooms.name.eq(room),'quantity'],errors='coerce').fillna(0).sum()
    days=pd.Period(f"{stay_year}-{stay_month:02d}").days_in_month
    return float(qty*days)

def _request_count(req, quotes, room, treatment, stay_year, stay_month, decision_date):
    q=quotes[(quotes.room_name==room)&(quotes.creation_datetime<=decision_date)]
    if treatment: q=q[q.arrangement_name==treatment]
    ids=set(q.request_code.dropna().astype(str))
    r=req[(req.stay_year==stay_year)&(req.stay_month_num==stay_month)&(req.creation_datetime<=decision_date)]
    return int(r[r.request_code.astype(str).isin(ids)].request_code.nunique())

def _historical_state(req,quotes,bookings,rooms,room,treatment,year,month,lead_days):
    rows=[]
    for py in range(2024,year):
        d=pd.Timestamp(py,month,1)-pd.Timedelta(days=lead_days)
        rc=_request_count(req,quotes,room,treatment,py,month,d)
        cr,_,_=_conversion_at_date(req,quotes,bookings,room,treatment,py,month,d)
        occ=_booked_room_nights_at_date(bookings,room,py,month,d)/max(_available_room_nights(rooms,room,py,month),1)*100
        rows.append((rc,cr,occ))
    if not rows: return np.nan,np.nan,np.nan
    return tuple(_prior_mean([r[i] for r in rows]) for i in range(3))

def _score(action_type, req_idx, cr_delta, occ, occ_hist, lead_days, cfg):
    tc=_timing_config(cfg); occ_delta=occ-occ_hist if pd.notna(occ_hist) else 0.0; cr_delta=cr_delta if pd.notna(cr_delta) else 0.0
    if action_type in {'PRICE_UP','PACKAGE_PRICE_UP'}:
        components=[np.clip((req_idx-1)/tc['request_index_scale'],-1,1) if pd.notna(req_idx) else 0,
                    np.clip(cr_delta/tc['conversion_delta_scale_pp'],-1,1),
                    np.clip(occ_delta/tc['occupancy_delta_scale_pp'],-1,1),
                    np.clip((occ-tc['neutral_occupancy_pct'])/tc['occupancy_level_scale_pp'],-1,1)]
    else:
        components=[np.clip((1-req_idx)/tc['request_index_scale'],-1,1) if pd.notna(req_idx) else 0,
                    np.clip(-cr_delta/tc['conversion_delta_scale_pp'],-1,1),
                    np.clip(-occ_delta/tc['occupancy_delta_scale_pp'],-1,1),
                    np.clip((tc['neutral_occupancy_pct']-occ)/tc['occupancy_level_scale_pp'],-1,1)]
    w=tc['weights']; score=sum(v*w[k] for v,k in zip(components,['request_pace','conversion','occupancy_pace','occupancy_level']))
    score += min(max(lead_days,0),180)/180*tc['lead_time_bonus']
    return float(score)

def _absolute_support(action_type, occ, cr, rc, tc):
    if rc < tc['min_current_requests']: return False
    if action_type in {'PRICE_UP','PACKAGE_PRICE_UP'}:
        return occ >= tc['absolute_price_up_occupancy_pct'] or (pd.notna(cr) and cr >= tc['absolute_price_up_conversion_pct'])
    return occ <= tc['absolute_price_down_occupancy_pct']

def _parse_transition(text):
    if not isinstance(text,str) or '→' not in text: return None,None
    left,right=[x.strip() for x in text.split('→',1)]
    return left,right

def _upsell_candidate_state(req,quotes,bookings,room,source,target,year,month,d):
    src=_request_count(req,quotes,room,source,year,month,d)
    tgt=_request_count(req,quotes,room,target,year,month,d)
    total=src+tgt
    share=100*tgt/total if total else np.nan
    cr,_,den=_conversion_at_date(req,quotes,bookings,room,target,year,month,d)
    return src,tgt,share,cr,den


def _signal_count(action_type, req_idx, cr_delta, occ, occ_hist, tc):
    """Count independent directional signals supporting the action."""
    count=0
    occ_delta=occ-occ_hist if pd.notna(occ_hist) else np.nan
    if action_type in {"PRICE_UP","PACKAGE_PRICE_UP"}:
        if pd.notna(req_idx) and req_idx >= tc["moderate_request_up_ratio"]: count+=1
        if pd.notna(cr_delta) and cr_delta >= tc["moderate_conversion_delta_pp"]: count+=1
        if pd.notna(occ_delta) and occ_delta >= tc["moderate_occupancy_delta_pp"]: count+=1
        if occ >= tc["absolute_price_up_occupancy_pct"]: count+=1
    else:
        if pd.notna(req_idx) and req_idx <= tc["moderate_request_down_ratio"]: count+=1
        if pd.notna(cr_delta) and cr_delta <= -tc["moderate_conversion_delta_pp"]: count+=1
        if pd.notna(occ_delta) and occ_delta <= -tc["moderate_occupancy_delta_pp"]: count+=1
        if occ <= tc["absolute_price_down_occupancy_pct"]: count+=1
    return count

def _month_key(ts):
    ts=pd.Timestamp(ts)
    return f"{ts.year:04d}-{ts.month:02d}"

def _infer_month_or_window(states, action_type, tc):
    """
    Infer coarser timing when an exact day is not defensible.

    MONTH:
      earliest calendar month with >= N evaluations, positive median directional
      score, and enough corroborating signals.

    WINDOW:
      earliest pair of adjacent calendar months with weaker but directionally
      consistent evidence.

    Returns a dict or None.
    """
    if not states:
        return None
    x=pd.DataFrame(states).copy()
    if x.empty: return None
    x["decision_month"]=pd.to_datetime(x["date"]).dt.to_period("M")
    groups=[]
    for period,g in x.groupby("decision_month",sort=True):
        groups.append({
            "period":period,
            "month":str(period),
            "first_date":pd.to_datetime(g["date"]).min(),
            "last_date":pd.to_datetime(g["date"]).max(),
            "evaluations":len(g),
            "median_score":float(g["score"].median()),
            "max_score":float(g["score"].max()),
            "median_signal_count":float(g["signal_count"].median()),
            "max_signal_count":int(g["signal_count"].max()),
            "mean_requests":float(g["rc"].mean()),
            "mean_req_idx":float(g["req_idx"].dropna().mean()) if g["req_idx"].notna().any() else np.nan,
            "mean_cr":float(g["cr"].dropna().mean()) if g["cr"].notna().any() else np.nan,
            "mean_hcr":float(g["hcr"].dropna().mean()) if g["hcr"].notna().any() else np.nan,
            "mean_occ":float(g["occ"].mean()),
            "mean_hocc":float(g["hocc"].dropna().mean()) if g["hocc"].notna().any() else np.nan,
        })

    # Earliest month with persistent, corroborated direction.
    for g in groups:
        if (g["evaluations"] >= tc["month_inference_min_evaluations"]
            and g["median_score"] >= tc["month_inference_score_threshold"]
            and g["max_signal_count"] >= tc["month_inference_min_signal_count"]):
            return {
                "precision":"MONTH",
                "period":g["month"],
                "status":"ESTIMATED_MONTH_TRIGGER",
                "confidence":"MEDIUM" if g["median_score"] >= tc["month_inference_score_threshold"]*1.5 else "LOW",
                "reason":(
                    f"Exact day was not robust, but {g['month']} shows persistent directional evidence "
                    f"across {g['evaluations']} evaluations (median timing score {g['median_score']:.2f}; "
                    f"up to {g['max_signal_count']} corroborating signals)."
                ),
                "summary":g,
            }

    # If no month qualifies, find the earliest adjacent two-month window.
    for a,b in zip(groups,groups[1:]):
        if b["period"].ordinal-a["period"].ordinal != 1:
            continue
        combined_score=(a["median_score"]+b["median_score"])/2
        combined_signals=max(a["max_signal_count"],b["max_signal_count"])
        if combined_score >= tc["window_inference_score_threshold"] and combined_signals >= 1:
            return {
                "precision":"WINDOW",
                "period":f"{a['month']} to {b['month']}",
                "status":"ESTIMATED_WINDOW_TRIGGER",
                "confidence":"LOW",
                "reason":(
                    f"No exact day or single month crossed the timing threshold, but directional evidence "
                    f"was consistently present across {a['month']}–{b['month']} "
                    f"(average monthly timing score {combined_score:.2f})."
                ),
                "summary":a,
            }
    return None

def _infer_upsell_month_or_window(states, tc):
    if not states:
        return None
    x=pd.DataFrame(states).copy()
    x["decision_month"]=pd.to_datetime(x["date"]).dt.to_period("M")
    groups=[]
    for period,g in x.groupby("decision_month",sort=True):
        groups.append({
            "period":period,
            "month":str(period),
            "evaluations":len(g),
            "median_score":float(g["score"].median()),
            "max_score":float(g["score"].max()),
            "mean_share":float(g["share"].dropna().mean()) if g["share"].notna().any() else np.nan,
            "mean_cr":float(g["cr"].dropna().mean()) if g["cr"].notna().any() else np.nan,
            "mean_src":float(g["src"].mean()),
            "mean_tgt":float(g["tgt"].mean()),
        })
    for g in groups:
        if g["evaluations"] >= 2 and g["median_score"] >= tc["upsell_month_score_threshold"]:
            return {
                "precision":"MONTH","period":g["month"],
                "status":"ESTIMATED_MONTH_UPSELL_TRIGGER",
                "confidence":"MEDIUM" if g["median_score"]>=tc["upsell_month_score_threshold"]*1.4 else "LOW",
                "reason":(
                    f"Exact upsell activation day was not robust, but {g['month']} shows persistent treatment-mix "
                    f"evidence (median activation score {g['median_score']:.2f}; "
                    f"target request share ~{g['mean_share']:.1f}%)."
                ),
                "summary":g,
            }
    for a,b in zip(groups,groups[1:]):
        if b["period"].ordinal-a["period"].ordinal != 1: continue
        avg=(a["median_score"]+b["median_score"])/2
        if avg >= tc["upsell_window_score_threshold"]:
            return {
                "precision":"WINDOW","period":f"{a['month']} to {b['month']}",
                "status":"ESTIMATED_WINDOW_UPSELL_TRIGGER","confidence":"LOW",
                "reason":(
                    f"No exact upsell date was defensible, but treatment-specific demand was directionally "
                    f"supportive across {a['month']}–{b['month']} (average activation score {avg:.2f})."
                ),
                "summary":a,
            }
    return None

def _apply_inferred_timing(row, inferred):
    row["timing_precision"]=inferred["precision"]
    row["timing_period"]=inferred["period"]
    row["timing_status"]=inferred["status"]
    row["timing_confidence"]=inferred["confidence"]
    row["timing_reason"]=inferred["reason"]
    row["decision_date"]=np.nan
    return row

def build_timed_actions(actions, bookings, requests, quotes, rooms, cfg):
    """
    Hierarchical timing:
      1. EXACT date when sustained multi-signal trigger exists.
      2. MONTH estimate when the direction is persistent at monthly level.
      3. WINDOW estimate when a two-month directional regime is visible.
      4. NONE only when timing cannot be supported even coarsely.

    Exact dates and estimated periods are deliberately distinguished so the
    report never presents inferred precision as factual precision.
    """
    tc=_timing_config(cfg); b=bookings.copy(); r=requests.copy(); q=quotes.copy()
    for x in (b,r):
        x["stay_year"]=x.checkin_date.dt.year
        x["stay_month_num"]=x.checkin_date.dt.month
    for x in (b,r,q):
        x["creation_datetime"]=_norm(x.creation_datetime)
    b["cancellation_datetime"]=_norm(b.cancellation_datetime)
    out=[]

    for _,a in actions.iterrows():
        row=a.to_dict()
        typ=a.action_type
        year=int(a.stay_year); month=int(a.stay_month_num)
        room=a.room_name; start=pd.Timestamp(year,month,1)

        row.update(
            timing_precision="NONE",
            timing_period=np.nan,
            decision_date=np.nan,
            timing_confidence="NOT_TIMED"
        )

        # ---- UPSELL timing -------------------------------------------------
        if typ=="PROMOTE_UPSELL":
            source,target=_parse_transition(str(a.treatment))
            candidates=[]
            all_states=[]
            if source and target:
                for lead in range(tc["max_lead_days"],tc["min_lead_days"]-1,-tc["evaluation_step_days"]):
                    d=start-pd.Timedelta(days=lead)
                    src,tgt,share,cr,den=_upsell_candidate_state(r,q,b,room,source,target,year,month,d)
                    score=min(
                        1.0,
                        0.45*((share if pd.notna(share) else 0)/tc["upsell_target_share_scale_pct"]) +
                        0.35*(tgt/tc["upsell_target_request_scale"]) +
                        0.20*((cr if pd.notna(cr) else 0)/tc["upsell_conversion_scale_pct"])
                    )
                    all_states.append(dict(date=d,lead=lead,src=src,tgt=tgt,share=share,cr=cr,score=score))

                    if src < tc["upsell_min_source_requests"] or tgt < tc["upsell_min_target_requests"]: continue
                    if share < tc["upsell_min_target_request_share_pct"]: continue
                    if pd.notna(cr) and cr < tc["upsell_min_target_conversion_pct"]: continue
                    candidates.append((d,lead,src,tgt,share,cr,score))

            chosen=None
            for i,c in enumerate(candidates):
                if i+1<len(candidates) and (candidates[i+1][0]-c[0]).days<=tc["sustain_days"]+tc["evaluation_step_days"]:
                    chosen=c; break

            if chosen:
                d,lead,src,tgt,share,cr,score=chosen
                conf="HIGH" if score>=tc["upsell_high_confidence_score"] else "MEDIUM"
                row.update(
                    decision_date=d.date().isoformat(),
                    timing_precision="EXACT",
                    timing_period=d.strftime("%Y-%m"),
                    lead_days_to_stay_month=lead,
                    timing_score=round(score,3),
                    timing_status="UPSELL_ACTIVATION_TRIGGER_FOUND",
                    timing_confidence=conf,
                    timing_reason=(
                        f"Earliest sustained upsell activation: {target} represented {share:.1f}% of "
                        f"{source}+{target} requests ({tgt} target vs {src} source requests); "
                        f"target conversion-to-date {cr:.1f}%."
                    ),
                    requests_to_date=src+tgt,
                    conversion_to_date_pct=round(cr,2) if pd.notna(cr) else np.nan
                )
            else:
                inferred=_infer_upsell_month_or_window(all_states,tc)
                if inferred:
                    row=_apply_inferred_timing(row,inferred)
                else:
                    row.update(
                        timing_status="NO_DEFENSIBLE_UPSELL_TIMING",
                        timing_reason=(
                            "Upsell opportunity exists retrospectively, but neither an exact date, a persistent "
                            "month, nor a two-month treatment-demand window can be supported from the historical state."
                        )
                    )
            out.append(row); continue

        # ---- PRICE / PACKAGE timing ---------------------------------------
        if typ not in PRICE_ACTIONS:
            row.update(
                timing_status="NOT_APPLICABLE",
                timing_reason="No timing model for this action type."
            )
            out.append(row); continue

        treatment=str(a.treatment) if pd.notna(a.treatment) and str(a.treatment).strip() else ""
        candidates=[]
        all_states=[]

        for lead in range(tc["max_lead_days"],tc["min_lead_days"]-1,-tc["evaluation_step_days"]):
            d=start-pd.Timedelta(days=lead)
            rc=_request_count(r,q,room,treatment,year,month,d)
            hrc,hcr,hocc=_historical_state(r,q,b,rooms,room,treatment,year,month,lead)
            cr,conv_n,conv_d=_conversion_at_date(r,q,b,room,treatment,year,month,d)
            occ=_booked_room_nights_at_date(b,room,year,month,d)/max(
                _available_room_nights(rooms,room,year,month),1
            )*100

            has_hist=pd.notna(hrc) and hrc>=tc["min_historical_requests"]
            req_idx=_safe_ratio(rc,hrc) if has_hist else np.nan
            cr_delta=cr-hcr if pd.notna(cr) and pd.notna(hcr) else np.nan
            score=_score(typ,req_idx,cr_delta,occ,hocc,lead,cfg)
            sig_count=_signal_count(typ,req_idx,cr_delta,occ,hocc,tc)

            all_states.append(dict(
                date=d,lead=lead,rc=rc,hrc=hrc,req_idx=req_idx,cr=cr,hcr=hcr,
                cr_delta=cr_delta,occ=occ,hocc=hocc,score=score,signal_count=sig_count
            ))

            historical_support=has_hist and score>=tc["score_threshold"]
            absolute_support=_absolute_support(typ,occ,cr,rc,tc) and score>=tc["absolute_score_threshold"]
            if historical_support or absolute_support:
                candidates.append((
                    d,lead,rc,hrc,req_idx,cr,hcr,cr_delta,occ,hocc,score,
                    conv_n,conv_d,has_hist,absolute_support
                ))

        chosen=None
        for i,c in enumerate(candidates):
            if i+1<len(candidates) and (candidates[i+1][0]-c[0]).days<=tc["sustain_days"]+tc["evaluation_step_days"]:
                chosen=c; break

        if chosen:
            d,lead,rc,hrc,ri,cr,hcr,cd,occ,hocc,score,cn,cdm,has_hist,abs_sup=chosen
            strong_hist=has_hist and hrc>=tc["high_confidence_historical_requests"]
            conf="HIGH" if score>=tc["high_confidence_score"] and (
                strong_hist or rc>=tc["high_confidence_current_requests"]
            ) else "MEDIUM"
            evidence="historical multi-signal" if has_hist else "within-season absolute demand state"
            row.update(
                decision_date=d.date().isoformat(),
                timing_precision="EXACT",
                timing_period=d.strftime("%Y-%m"),
                lead_days_to_stay_month=lead,
                requests_to_date=rc,
                historical_requests_same_lead=round(hrc,1) if pd.notna(hrc) else np.nan,
                request_pace_index=round(ri,3) if pd.notna(ri) else np.nan,
                conversion_to_date_pct=round(cr,2) if pd.notna(cr) else np.nan,
                historical_conversion_same_lead_pct=round(hcr,2) if pd.notna(hcr) else np.nan,
                conversion_delta_pp=round(cd,2) if pd.notna(cd) else np.nan,
                occupancy_on_books_pct=round(occ,2),
                historical_occupancy_same_lead_pct=round(hocc,2) if pd.notna(hocc) else np.nan,
                timing_score=round(score,3),
                timing_status="DECISION_TRIGGER_FOUND",
                timing_confidence=conf,
                timing_reason=(
                    f"Earliest sustained {evidence} trigger: request pace {ri:.2f}x historical; "
                    f"conversion {cr:.1f}% vs {hcr:.1f}% historical; occupancy-on-books "
                    f"{occ:.1f}% vs {hocc:.1f}% historical at the same lead time."
                    if has_hist else
                    f"Earliest sustained within-season trigger: {rc} requests, conversion-to-date "
                    f"{cr:.1f}%, occupancy-on-books {occ:.1f}% with {lead} days to stay month."
                )
            )
        else:
            inferred=_infer_month_or_window(all_states,typ,tc)
            if inferred:
                row=_apply_inferred_timing(row,inferred)
            else:
                row.update(
                    timing_status="NO_DEFENSIBLE_TIMING",
                    timing_reason=(
                        "Retrospective action exists, but the historical state does not support an exact date, "
                        "a persistent intervention month, or a two-month intervention window. No timing is fabricated."
                    )
                )
        out.append(row)

    result=pd.DataFrame(out)
    # Presentation-friendly label.
    result["decision_timing"]=np.select(
        [
            result["timing_precision"].eq("EXACT"),
            result["timing_precision"].eq("MONTH"),
            result["timing_precision"].eq("WINDOW"),
        ],
        [
            result["decision_date"].astype(str),
            result["timing_period"].astype(str),
            result["timing_period"].astype(str),
        ],
        default="INSUFFICIENT EVIDENCE"
    )
    return result
