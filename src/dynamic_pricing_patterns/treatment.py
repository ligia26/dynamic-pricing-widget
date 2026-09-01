
from __future__ import annotations
import numpy as np
import pandas as pd
from .data import enrich_bookings
from .utils import confidence_from_score

def treatment_cells(bookings, conv_requests, quotes, as_of, min_bookings):
    b=enrich_bookings(bookings)
    hist=b[(b["status"].eq("CONFIRMED")) & (b["checkin_date"]<=as_of)].copy()
    keys=["stay_year","stay_month_num","season","booking_window","arrangement_name"]
    cells=(hist.groupby(keys,dropna=False).agg(
        bookings=("booking_code","nunique"),
        room_nights=("room_nights","sum"),
        revenue=("total_stay_amount","sum"),
        avg_adr=("adr","mean"),
        avg_lead_days=("lead_time_days","mean")
    ).reset_index())
    cells["realized_adr"]=np.where(cells["room_nights"]>0,cells["revenue"]/cells["room_nights"],np.nan)

    allb=b.groupby(keys,dropna=False).agg(
        all_bookings=("booking_code","nunique"),
        canceled=("is_canceled","sum")
    ).reset_index()
    allb["cancellation_pct"]=100*allb["canceled"]/allb["all_bookings"].clip(lower=1)
    cells=cells.merge(allb[keys+["cancellation_pct"]],on=keys,how="left",validate="one_to_one")

    # Directional same-treatment conversion from quote -> booked treatment.
    req=conv_requests.copy()
    q=quotes[["request_code","arrangement_name"]].drop_duplicates().rename(
        columns={"arrangement_name":"arrangement_name_quoted"}
    )
    qr=req.merge(q,on="request_code",how="inner")
    confirmed=bookings[bookings["status"].eq("CONFIRMED")][
        ["customer_code","checkin_date","arrangement_name"]
    ].drop_duplicates().rename(columns={"arrangement_name":"arrangement_name_booked"})
    m=qr.merge(confirmed,on=["customer_code","checkin_date"],how="left")
    m["same_treatment"]=m["arrangement_name_booked"].eq(m["arrangement_name_quoted"]).astype(int)
    m["stay_year"]=pd.to_datetime(m["checkin_date"]).dt.year
    m["stay_month_num"]=pd.to_datetime(m["checkin_date"]).dt.month
    from .utils import season, booking_window
    m["season"]=m["stay_month_num"].map(season)
    if "lead_time_days" in m:
        m["booking_window"]=m["lead_time_days"].map(booking_window)
    else:
        m["booking_window"]="UNKNOWN"
    cg=(m.groupby(
        ["stay_year","stay_month_num","season","booking_window","arrangement_name_quoted"],
        dropna=False
    ).agg(
        quoted_requests=("request_code","nunique"),
        same_treatment_converted=("same_treatment","sum")
    ).reset_index().rename(columns={"arrangement_name_quoted":"arrangement_name"}))
    cg["conversion_pct"]=np.where(cg["quoted_requests"]>0,100*cg["same_treatment_converted"]/cg["quoted_requests"],np.nan)
    cells=cells.merge(cg,on=keys,how="left",validate="one_to_one")
    return cells[cells["bookings"]>=min_bookings].copy()

def discover_treatment_opportunities(cells,cfg):
    comp_keys=["arrangement_name","stay_month_num","season","booking_window"]
    c=cells.copy()
    q=float(cfg["benchmark_quantile"])
    bench=(c.groupby(comp_keys).agg(
        benchmark_adr=("realized_adr",lambda s:s.quantile(q)),
        comparable_years=("stay_year","nunique"),
        comparable_conversion=("conversion_pct","median"),
        comparable_cancel=("cancellation_pct","median")
    ).reset_index())
    c=c.merge(bench,on=comp_keys,how="left",validate="many_to_one")
    c["adr_gap"]=c["benchmark_adr"]-c["realized_adr"]
    c["adr_gap_pct"]=c["adr_gap"]/c["realized_adr"].replace(0,np.nan)
    c["raw_gross_opportunity"]=c["adr_gap"].clip(lower=0)*c["room_nights"]
    c["conversion_supported"]=(
        c["conversion_pct"].isna()|c["comparable_conversion"].isna()|
        (c["conversion_pct"]>=cfg["conversion_support_ratio"]*c["comparable_conversion"])
    )
    c["cancel_supported"]=c["cancellation_pct"].fillna(0)<=cfg["cancellation_penalty_threshold_pct"]

    def conf(r):
        score=0
        score += int(r["comparable_years"]>=cfg["min_years_for_high_confidence"])
        score += int(r["bookings"]>=20)
        score += int(pd.notna(r["quoted_requests"]) and r["quoted_requests"]>=40)
        score += int(r["conversion_supported"])
        score += int(r["cancel_supported"])
        return confidence_from_score(score)
    c["confidence"]=c.apply(conf,axis=1)
    c["max_uplift_pct"]=c["adr_gap_pct"].clip(lower=0,upper=float(cfg["max_recommended_uplift_pct"]))
    c["decision"]=np.select([
        (c["adr_gap_pct"]>=0.05)&c["conversion_supported"]&c["cancel_supported"],
        (c["adr_gap_pct"]>=0.02)&c["conversion_supported"]
    ],["INCREASE","TEST_SMALL_INCREASE"],default="HOLD")
    return c.sort_values("raw_gross_opportunity",ascending=False)

def simulate_treatment(opps,cfg):
    rows=[]
    for _,r in opps.iterrows():
        if r["decision"]=="HOLD" or r["raw_gross_opportunity"]<=0:
            continue
        for name,s in cfg["scenarios"].items():
            # keep treatment impact conservative and separate from room total
            uplift=min(r["max_uplift_pct"]*s["capture_rate"],cfg["max_recommended_uplift_pct"])
            sim_adr=r["realized_adr"]*(1+uplift)
            retained=r["room_nights"]*s["volume_retention"]
            impact=sim_adr*retained-r["revenue"]
            rows.append({
                "scenario":name,
                "arrangement_name":r["arrangement_name"],
                "stay_year":int(r["stay_year"]),
                "stay_month_num":int(r["stay_month_num"]),
                "booking_window":r["booking_window"],
                "confidence":r["confidence"],
                "historical_revenue":round(r["revenue"],2),
                "historical_adr":round(r["realized_adr"],2),
                "benchmark_adr":round(r["benchmark_adr"],2),
                "simulated_adr":round(sim_adr,2),
                "incremental_revenue":round(impact,2),
                "note":"NON-ADDITIVE with room opportunity totals; same stay revenue base."
            })
    return pd.DataFrame(rows)
