
from __future__ import annotations
import numpy as np
import pandas as pd
from .data import enrich_bookings, sellable_rooms

DEFAULT_HORIZONS = (180,120,90,60,30,14,7,0)

def _capacity_by_room(rooms):
    s=sellable_rooms(rooms)
    return s[["id","name","quantity"]].rename(
        columns={"id":"room_id","name":"room_name","quantity":"capacity"}
    )

def _nearest_horizon(days_to_arrival: int, horizons=DEFAULT_HORIZONS) -> int:
    vals=np.array(horizons, dtype=int)
    return int(vals[np.argmin(np.abs(vals-int(days_to_arrival)))])

def build_daily_inventory(bookings, daily_revenue, rooms, as_of):
    cap=_capacity_by_room(rooms)
    b=enrich_bookings(bookings)
    active=b[b["status"].eq("CONFIRMED")][
        ["booking_code","room_id","room_name","creation_datetime","checkin_date","checkout_date"]
    ].copy()

    d=daily_revenue[
        (daily_revenue["status"].eq("CONFIRMED")) &
        (daily_revenue["in_stay_range"].eq(1))
    ].copy()
    d=d.merge(
        active[["booking_code","creation_datetime"]],
        on="booking_code",how="inner",validate="many_to_one"
    )
    d=d.merge(
        cap[["room_id","room_name","capacity"]],
        on="room_id",how="left",validate="many_to_one"
    )
    d=d[d["capacity"].notna()].copy()

    snap=d[d["creation_datetime"]<=as_of].copy()
    g=(snap.groupby(["stay_date","room_id"]).agg(
        room_name=("room_name","first"),
        capacity=("capacity","first"),
        on_books_rooms=("booking_code","nunique"),
        on_books_revenue=("stay_amount","sum")
    ).reset_index())

    g["occupancy_on_books_pct"]=100*g["on_books_rooms"]/g["capacity"].replace(0,np.nan)
    g["adr_on_books"]=g["on_books_revenue"]/g["on_books_rooms"].replace(0,np.nan)
    g["remaining_rooms"]=(g["capacity"]-g["on_books_rooms"]).clip(lower=0)
    g["capacity_exception"]=g["on_books_rooms"]>g["capacity"]
    return g

def build_pickup_curve(bookings, daily_revenue, rooms, as_of, horizons=DEFAULT_HORIZONS):
    """
    Reconstruct historical daily on-books snapshots at comparable days-to-arrival.

    Unit of comparison is now:
      historical stay_date × room × horizon_days

    This matches the current observation unit (future stay_date × room), avoiding
    the invalid monthly-vs-daily comparison.
    """
    cap=_capacity_by_room(rooms)
    b=enrich_bookings(bookings)
    confirmed=b[b["status"].eq("CONFIRMED")][
        ["booking_code","room_id","creation_datetime"]
    ].copy()

    d=daily_revenue[
        (daily_revenue["status"].eq("CONFIRMED")) &
        (daily_revenue["in_stay_range"].eq(1)) &
        (daily_revenue["stay_date"]<=as_of)
    ].copy()
    d=d.merge(
        confirmed,on=["booking_code","room_id"],how="inner",validate="many_to_one"
    )
    d=d.merge(
        cap[["room_id","room_name","capacity"]],
        on="room_id",how="inner",validate="many_to_one"
    )
    d["stay_month_num"]=d["stay_date"].dt.month
    d["stay_year"]=d["stay_date"].dt.year

    final=(d.groupby(
        ["stay_date","stay_year","stay_month_num","room_id","room_name","capacity"]
    ).agg(
        final_occupied_rooms=("booking_code","nunique"),
        final_revenue=("stay_amount","sum")
    ).reset_index())

    rows=[]
    for h in horizons:
        cutoff=d["stay_date"]-pd.to_timedelta(h,unit="D")
        on=d[d["creation_datetime"]<=cutoff].copy()
        g=(on.groupby(
            ["stay_date","stay_year","stay_month_num","room_id","room_name","capacity"]
        ).agg(
            rooms_on_books=("booking_code","nunique"),
            revenue_on_books=("stay_amount","sum")
        ).reset_index())
        g=final.merge(
            g,
            on=["stay_date","stay_year","stay_month_num","room_id","room_name","capacity"],
            how="left",
            validate="one_to_one"
        )
        g["rooms_on_books"]=g["rooms_on_books"].fillna(0)
        g["revenue_on_books"]=g["revenue_on_books"].fillna(0)
        g["horizon_days"]=h
        g["remaining_pickup_rooms"]=(
            g["final_occupied_rooms"]-g["rooms_on_books"]
        ).clip(lower=0)
        g["otb_saturation_pct"]=100*g["rooms_on_books"]/g["capacity"].replace(0,np.nan)
        g["final_occupancy_pct"]=100*g["final_occupied_rooms"]/g["capacity"].replace(0,np.nan)
        rows.append(g)

    return pd.concat(rows,ignore_index=True) if rows else pd.DataFrame()

def historical_pickup_baseline(pickup):
    if pickup.empty:
        return pd.DataFrame()
    keys=["room_name","stay_month_num","horizon_days"]
    out=(pickup.groupby(keys).agg(
        historical_otb_rooms=("rooms_on_books","median"),
        historical_final_occupied_rooms=("final_occupied_rooms","median"),
        historical_expected_remaining_rooms=("remaining_pickup_rooms","median"),
        historical_otb_saturation_pct=("otb_saturation_pct","median"),
        historical_final_occupancy_pct=("final_occupancy_pct","median"),
        comparable_years=("stay_year","nunique"),
        comparable_stay_dates=("stay_date","nunique")
    ).reset_index())
    return out

def current_observations(bookings, daily_revenue, rooms, historical_cells, pickup, cfg, as_of):
    inv=build_daily_inventory(bookings,daily_revenue,rooms,as_of)
    if inv.empty:
        return pd.DataFrame()

    future=inv[inv["stay_date"]>as_of].copy()
    future["days_to_arrival"]=(future["stay_date"]-as_of).dt.days.astype(int)
    future["stay_month_num"]=future["stay_date"].dt.month
    future["stay_year"]=future["stay_date"].dt.year
    future["pickup_horizon_days"]=future["days_to_arrival"].map(_nearest_horizon)

    hist=(historical_cells.groupby(["room_name","stay_month_num"]).agg(
        historical_adr=("realized_adr","median"),
        high_adr=("realized_adr",lambda s:s.quantile(.75)),
        historical_conversion=("conversion_pct","median"),
        historical_cancellation=("cancellation_pct","median")
    ).reset_index())
    future=future.merge(
        hist,on=["room_name","stay_month_num"],how="left",validate="many_to_one"
    )

    pickup_base=historical_pickup_baseline(pickup)
    future=future.merge(
        pickup_base,
        left_on=["room_name","stay_month_num","pickup_horizon_days"],
        right_on=["room_name","stay_month_num","horizon_days"],
        how="left",
        validate="many_to_one"
    )

    # pace index compares current OTB with historical expected OTB at same horizon
    future["pace_vs_history_pct"]=100*(
        future["on_books_rooms"]-future["historical_otb_rooms"]
    )/future["historical_otb_rooms"].replace(0,np.nan)

    # Expected remaining demand:
    # historical expected remaining bookings adjusted by current pace.
    # We cap pace adjustment to avoid unstable extrapolation.
    pace_factor=(1+future["pace_vs_history_pct"].fillna(0)/100).clip(lower=0.60,upper=1.40)
    future["expected_remaining_demand_rooms"]=(
        future["historical_expected_remaining_rooms"].fillna(0)*pace_factor
    )
    # Cannot sell more than currently uncommitted physical capacity.
    future["expected_remaining_demand_rooms"]=np.minimum(
        future["expected_remaining_demand_rooms"],
        future["remaining_rooms"]
    ).clip(lower=0)

    price_gap=(future["high_adr"]-future["adr_on_books"])/future["adr_on_books"].replace(0,np.nan)
    future["price_gap_to_high_pct"]=100*price_gap

    sat=future["occupancy_on_books_pct"]
    pace=future["pace_vs_history_pct"].fillna(0)

    conditions=[
        (future["capacity_exception"]),
        (sat>=80)&(pace>=10)&(price_gap>=0.05),
        (sat>=65)&(pace>=0)&(price_gap>=0.03),
        (sat<35)&(pace<=-10)&(future["days_to_arrival"]<=30),
        (price_gap<=-0.05)
    ]
    choices=["CAPACITY_EXCEPTION","INCREASE","TEST_INCREASE","PROTECT_VOLUME","HOLD_HIGH"]
    future["decision"]=np.select(conditions,choices,default="HOLD")

    max_up=100*float(cfg["max_recommended_uplift_pct"])
    future["suggested_uplift_pct"]=np.select(
        [
            future["decision"].eq("INCREASE"),
            future["decision"].eq("TEST_INCREASE")
        ],
        [
            np.minimum(100*price_gap.clip(lower=0),max_up),
            np.minimum(100*price_gap.clip(lower=0)*0.5,max_up)
        ],
        default=0.0
    )

    future["recommended_adr"]=(
        future["adr_on_books"].fillna(future["historical_adr"])*
        (1+future["suggested_uplift_pct"]/100)
    )

    future["incremental_adr_eur"]=(
        future["recommended_adr"]-
        future["adr_on_books"].fillna(future["historical_adr"])
    ).clip(lower=0)

    # Expected forward impact = expected remaining demand × incremental ADR.
    # This is explicitly conditional on the historical-pickup demand estimate.
    future["expected_incremental_revenue_eur"]=(
        future["expected_remaining_demand_rooms"]*
        future["incremental_adr_eur"]
    ).round(2)

    base_adr=future["adr_on_books"].fillna(future["historical_adr"])
    future["break_even_demand_loss_pct"]=np.where(
        future["recommended_adr"]>0,
        100*(1-base_adr/future["recommended_adr"]),
        0
    )

    # Confidence:
    # - comparable historical years
    # - no capacity exception
    # - meaningful historical OTB baseline
    # - decision supported by both pace and price
    score=(
        (future["comparable_years"].fillna(0)>=2).astype(int) +
        (~future["capacity_exception"]).astype(int) +
        (future["comparable_stay_dates"].fillna(0)>=10).astype(int) +
        (future["expected_remaining_demand_rooms"]>0).astype(int) +
        (future["price_gap_to_high_pct"].fillna(0)>=3).astype(int)
    )
    future["confidence"]=np.select(
        [score>=4,score>=3],
        ["HIGH","MEDIUM"],
        default="LOW"
    )

    # Don't state expected € impact for anomalous capacity rows.
    future.loc[future["capacity_exception"],"expected_incremental_revenue_eur"]=np.nan

    future["reason"]=future.apply(lambda r:
        (
            f"OTB saturation {r['occupancy_on_books_pct']:.1f}%; "
            f"pace vs historical {r['pace_vs_history_pct']:.1f}% at ~{int(r['pickup_horizon_days'])}d horizon; "
            f"ADR {r['adr_on_books']:.2f} vs historical high {r['high_adr']:.2f}; "
            f"expected remaining demand {r['expected_remaining_demand_rooms']:.2f} rooms; "
            f"{int(r['days_to_arrival'])} days to arrival."
        ) if not r["capacity_exception"] else
        (
            f"Capacity exception: {int(r['on_books_rooms'])} OTB rooms vs "
            f"{int(r['capacity'])} current catalog capacity. Pricing impact suppressed."
        )
    ,axis=1)

    cols=[
        "stay_date","room_id","room_name","capacity","on_books_rooms",
        "remaining_rooms","occupancy_on_books_pct","days_to_arrival",
        "pickup_horizon_days","historical_otb_rooms",
        "historical_final_occupied_rooms","pace_vs_history_pct",
        "expected_remaining_demand_rooms","adr_on_books","historical_adr",
        "high_adr","price_gap_to_high_pct","decision","suggested_uplift_pct",
        "recommended_adr","incremental_adr_eur",
        "expected_incremental_revenue_eur","break_even_demand_loss_pct",
        "confidence","capacity_exception","reason"
    ]
    return future[cols].sort_values(["stay_date","room_name"])

def observation_summary(obs):
    if obs.empty:
        return pd.DataFrame()
    x=obs[~obs["capacity_exception"]].copy()
    return (x.groupby(["room_name","decision","confidence"]).agg(
        stay_dates=("stay_date","nunique"),
        remaining_rooms=("remaining_rooms","sum"),
        expected_remaining_demand_rooms=("expected_remaining_demand_rooms","sum"),
        expected_incremental_revenue_eur=("expected_incremental_revenue_eur","sum"),
        avg_pace_vs_history_pct=("pace_vs_history_pct","mean"),
        avg_saturation_pct=("occupancy_on_books_pct","mean"),
        avg_suggested_uplift_pct=("suggested_uplift_pct","mean")
    ).reset_index().sort_values(
        "expected_incremental_revenue_eur",ascending=False
    ))
