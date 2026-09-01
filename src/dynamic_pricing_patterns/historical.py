
from __future__ import annotations
import numpy as np
import pandas as pd
from .data import enrich_bookings
from .utils import confidence_from_score

def historical_cells(bookings, conv, as_of, min_bookings):
    allb=enrich_bookings(bookings)
    hist=allb[(allb["status"].eq("CONFIRMED"))&(allb["checkin_date"]<=as_of)].copy()
    keys=["stay_year","stay_month_num","season","booking_window","room_name"]
    cells=(hist.groupby(keys,dropna=False).agg(
        bookings=("booking_code","nunique"),
        room_nights=("room_nights","sum"),
        revenue=("total_stay_amount","sum"),
        avg_adr=("adr","mean"),
        avg_lead_days=("lead_time_days","mean")
    ).reset_index())
    cells["realized_adr"]=np.where(cells["room_nights"]>0,cells["revenue"]/cells["room_nights"],np.nan)

    allcells=(allb.groupby(keys,dropna=False).agg(
        all_bookings=("booking_code","nunique"), canceled=("is_canceled","sum")
    ).reset_index())
    allcells["cancellation_pct"]=100*allcells["canceled"]/allcells["all_bookings"].clip(lower=1)
    cells=cells.merge(allcells[keys+["cancellation_pct"]],on=keys,how="left",validate="one_to_one")
    cells=cells.merge(conv[keys+["quoted_requests","conversion_pct"]],on=keys,how="left",validate="one_to_one")
    return cells[cells["bookings"]>=min_bookings].copy()

def discover_opportunities(cells,cfg):
    comp_keys=["room_name","stay_month_num","season","booking_window"]
    c=cells.copy()
    q=float(cfg["benchmark_quantile"])
    bench=(c.groupby(comp_keys).agg(
        benchmark_adr=("realized_adr",lambda s:s.quantile(q)),
        comparable_years=("stay_year","nunique"),
        comparable_volume=("room_nights","sum"),
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
        (c["adr_gap_pct"]>=0.02)&c["conversion_supported"],
    ],["INCREASE","TEST_SMALL_INCREASE"],default="HOLD")
    c["reason"]=c.apply(lambda r:
        f"ADR {r['realized_adr']:.2f} vs benchmark {r['benchmark_adr']:.2f}; "
        f"gap {max(r['adr_gap_pct'],0)*100:.1f}%; conversion "
        f"{'supports' if r['conversion_supported'] else 'does not support'} uplift; "
        f"cancellation {r['cancellation_pct']:.1f}%.",axis=1)
    return c.sort_values("raw_gross_opportunity",ascending=False)
