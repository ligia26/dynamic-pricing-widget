
from __future__ import annotations
import numpy as np
import pandas as pd

def build_remaining_horizon_opportunities(obs, cfg):
    """
    Converts current observations into a portfolio view.

    Immediate live impact:
      only explicit INCREASE / TEST_INCREASE decisions.

    Remaining-horizon modeled opportunity:
      includes lower-confidence MONITOR_UP opportunities when:
      - current ADR is below contextual historical high,
      - expected remaining demand exists,
      - current pace is not materially behind,
      - no capacity exception.

    This is intentionally separate from immediate expected impact.
    """
    if obs.empty:
        return pd.DataFrame()

    x=obs.copy()
    max_up=100*float(cfg["max_recommended_uplift_pct"])

    monitor=(
        ~x["capacity_exception"] &
        x["decision"].isin(["HOLD","HOLD_HIGH"]) &
        (x["price_gap_to_high_pct"]>=3) &
        (x["expected_remaining_demand_rooms"]>0) &
        (x["pace_vs_history_pct"].fillna(0)>=-10)
    )
    x["portfolio_action"]=x["decision"]
    x.loc[monitor,"portfolio_action"]="MONITOR_UP"

    # For monitor opportunities, capture only 30% of the observed price gap.
    x["portfolio_uplift_pct"]=x["suggested_uplift_pct"].fillna(0)
    x.loc[monitor,"portfolio_uplift_pct"]=np.minimum(
        x.loc[monitor,"price_gap_to_high_pct"]*0.30,
        max_up*0.60
    )

    base=x["adr_on_books"].fillna(x["historical_adr"])
    x["portfolio_recommended_adr"]=base*(1+x["portfolio_uplift_pct"]/100)
    x["portfolio_incremental_adr"]=(
        x["portfolio_recommended_adr"]-base
    ).clip(lower=0)
    x["remaining_horizon_impact_eur"]=(
        x["expected_remaining_demand_rooms"]*
        x["portfolio_incremental_adr"]
    ).round(2)

    # Realization weight makes weaker monitor opportunities explicit.
    weights={"HIGH":1.0,"MEDIUM":0.75,"LOW":0.50}
    x["confidence_weight"]=x["confidence"].map(weights).fillna(0.5)
    x.loc[x["portfolio_action"].eq("MONITOR_UP"),"confidence_weight"]*=0.65
    x["risk_adjusted_horizon_impact_eur"]=(
        x["remaining_horizon_impact_eur"]*x["confidence_weight"]
    ).round(2)

    x.loc[x["capacity_exception"],[
        "remaining_horizon_impact_eur","risk_adjusted_horizon_impact_eur"
    ]]=np.nan

    return x.sort_values("risk_adjusted_horizon_impact_eur",ascending=False)

def portfolio_summary(portfolio):
    if portfolio.empty:
        return pd.DataFrame()
    x=portfolio[~portfolio["capacity_exception"]].copy()
    return (x.groupby(["room_name","portfolio_action"]).agg(
        stay_dates=("stay_date","nunique"),
        expected_remaining_demand_rooms=("expected_remaining_demand_rooms","sum"),
        gross_horizon_impact_eur=("remaining_horizon_impact_eur","sum"),
        risk_adjusted_horizon_impact_eur=("risk_adjusted_horizon_impact_eur","sum"),
        avg_uplift_pct=("portfolio_uplift_pct","mean")
    ).reset_index().sort_values("risk_adjusted_horizon_impact_eur",ascending=False))
