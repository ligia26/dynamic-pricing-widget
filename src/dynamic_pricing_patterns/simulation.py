
from __future__ import annotations
import numpy as np
import pandas as pd
from .constants import CONF_RANK

def simulate(opps,cfg):
    rows=[]
    for _,r in opps.iterrows():
        if r["decision"]=="HOLD" or r["raw_gross_opportunity"]<=0:
            continue
        for name,s in cfg["scenarios"].items():
            if CONF_RANK[r["confidence"]]<CONF_RANK[s["min_confidence"]]:
                continue
            uplift=min(r["max_uplift_pct"]*s["capture_rate"],cfg["max_recommended_uplift_pct"])
            sim_adr=r["realized_adr"]*(1+uplift)
            retained=r["room_nights"]*s["volume_retention"]
            sim_rev=sim_adr*retained
            impact=sim_rev-r["revenue"]
            break_even_retention=r["realized_adr"]/sim_adr if sim_adr>0 else 1
            rows.append({
                "scenario":name,"room_name":r["room_name"],"stay_year":int(r["stay_year"]),
                "stay_month_num":int(r["stay_month_num"]),"season":r["season"],
                "booking_window":r["booking_window"],"decision":r["decision"],
                "confidence":r["confidence"],"historical_room_nights":round(r["room_nights"],2),
                "historical_adr":round(r["realized_adr"],2),"benchmark_adr":round(r["benchmark_adr"],2),
                "simulated_adr":round(sim_adr,2),"applied_uplift_pct":round(100*uplift,2),
                "assumed_volume_retention_pct":round(100*s["volume_retention"],2),
                "historical_revenue":round(r["revenue"],2),"simulated_revenue":round(sim_rev,2),
                "incremental_revenue":round(impact,2),
                "incremental_revenue_pct":round(100*impact/r["revenue"],2) if r["revenue"] else np.nan,
                "break_even_volume_loss_pct":round(100*(1-break_even_retention),2),
                "reason":r["reason"]
            })
    return pd.DataFrame(rows)

def aggregate(sim):
    if sim.empty: return pd.DataFrame()
    rec=sim[sim["scenario"].eq("recommended")].copy()
    if rec.empty: rec=sim.copy()
    out=(rec.groupby("room_name").agg(
        opportunities=("room_name","size"),historical_revenue=("historical_revenue","sum"),
        simulated_revenue=("simulated_revenue","sum"),incremental_revenue=("incremental_revenue","sum")
    ).reset_index())
    out["incremental_revenue_pct"]=100*out["incremental_revenue"]/out["historical_revenue"].replace(0,np.nan)
    return out.sort_values("incremental_revenue",ascending=False)
