
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from .data import load_data
from .conversion import build_conversion
from .historical import historical_cells, discover_opportunities
from .simulation import simulate, aggregate
from .observations import build_pickup_curve, current_observations, observation_summary
from .portfolio import build_remaining_horizon_opportunities, portfolio_summary
from .treatment import treatment_cells, discover_treatment_opportunities, simulate_treatment
from .revpar import monthly_room_dynamics, yoy_dynamics, optimize_revpar, yearly_opportunity
from .treatment_strategy import treatment_context_dynamics, treatment_price_recommendations, treatment_promotion_candidates, upsell_evidence
from .action_catalog import build_action_catalog
from .decision_timing import build_timed_actions
from .daily_pricing import build_pricing_trajectory

def run(input_dir: Path, output_dir: Path, config_path: Path):
    cfg=json.loads(config_path.read_text())
    as_of=pd.Timestamp(cfg["as_of_date"])
    b,r,q,rooms,treatments,daily=load_data(input_dir)

    # Non-critical source anomalies are made visible in outputs rather than hidden.
    validation_report=pd.DataFrame([{
        "metric":"negative_stay_amount_rows",
        "value":int((pd.to_numeric(b["total_stay_amount"],errors="coerce")<0).sum()),
        "severity":"WARNING",
        "handling":"Retained; source may contain legitimate adjustments/refunds."
    }])

    conv=build_conversion(b,r,q)
    cells=historical_cells(b,conv,as_of,cfg["min_bookings_per_cell"])
    opps=discover_opportunities(cells,cfg)
    sim=simulate(opps,cfg)
    ranking=aggregate(sim)

    pickup=build_pickup_curve(b,daily,rooms,as_of)
    obs=current_observations(b,daily,rooms,cells,pickup,cfg,as_of)
    obs_summary=observation_summary(obs)
    portfolio=build_remaining_horizon_opportunities(obs,cfg)
    portfolio_sum=portfolio_summary(portfolio)
    tcells=treatment_cells(b,r,q,as_of,cfg['min_bookings_per_cell'])
    topps=discover_treatment_opportunities(tcells,cfg)
    tsim=simulate_treatment(topps,cfg)

    # v0.5: year-by-year price-volume / RevPAR optimization.
    monthly=monthly_room_dynamics(b,rooms,conv,as_of)
    yoy=yoy_dynamics(monthly)
    revpar_recs=optimize_revpar(yoy,cfg['revpar_optimization'])
    yearly=yearly_opportunity(revpar_recs)
    tdyn=treatment_context_dynamics(b,as_of)
    trecs=treatment_price_recommendations(tdyn,cfg['revpar_optimization'])
    promotions=treatment_promotion_candidates(tdyn,cfg['revpar_optimization'])
    upsell=upsell_evidence(b,as_of)
    actions=build_action_catalog(revpar_recs,trecs,promotions)
    timed_actions=build_timed_actions(actions,b,r,q,rooms,cfg)
    pricing_trajectory=build_pricing_trajectory(actions,b,r,q,rooms,cfg)

    output_dir.mkdir(parents=True,exist_ok=True)
    outputs={
        "conversion_context.csv":conv,
        "historical_cells.csv":cells,
        "opportunity_candidates.csv":opps,
        "scenario_results.csv":sim,
        "opportunity_ranking.csv":ranking,
        "historical_pickup_curve.csv":pickup,
        "current_observations.csv":obs,
        "observation_summary.csv":obs_summary,
        "remaining_horizon_opportunities.csv":portfolio,
        "remaining_horizon_summary.csv":portfolio_sum,
        "treatment_historical_cells.csv":tcells,
        "treatment_opportunity_candidates.csv":topps,
        "treatment_scenario_results.csv":tsim,
        "room_monthly_dynamics.csv":monthly,
        "room_yoy_dynamics.csv":yoy,
        "revpar_recommendations.csv":revpar_recs,
        "yearly_economic_opportunity.csv":yearly,
        "treatment_context_dynamics.csv":tdyn,
        "treatment_price_recommendations.csv":trecs,
        "treatment_promotion_candidates.csv":promotions,
        "treatment_upsell_evidence.csv":upsell,
        "actionable_recommendations.csv":actions,
        "timed_actionable_recommendations.csv":timed_actions,
        "pricing_trajectory.csv":pricing_trajectory,
        "validation_report.csv":validation_report,
    }
    for name,df in outputs.items():
        df.to_csv(output_dir/name,index=False)

    summary={
        "version":"1.1.0",
        "timed_actions_total":int(len(timed_actions)),
        "pricing_trajectory_steps":int(len(pricing_trajectory)),
        "pricing_actions_with_trajectory":int(pricing_trajectory["source_action_id"].nunique()) if not pricing_trajectory.empty else 0,
        "timed_actions_with_decision_date":int(timed_actions["decision_date"].notna().sum()),
        "timed_price_package_actions":int(timed_actions["action_type"].isin(["PRICE_UP","PRICE_DOWN","PACKAGE_PRICE_UP"]).sum()),
        "as_of_date":str(as_of.date()),
        "historical_cells":int(len(cells)),
        "candidate_increase_cells":int((opps["decision"]!="HOLD").sum()),
        "recommended_incremental_revenue":round(float(
            sim.loc[sim["scenario"].eq("recommended"),"incremental_revenue"].sum()
        ),2) if not sim.empty else 0.0,
        "future_observation_rows":int(len(obs)),
        "future_action_rows":int(obs["decision"].isin(["INCREASE","TEST_INCREASE","PROTECT_VOLUME"]).sum()) if not obs.empty else 0,
        "expected_live_incremental_revenue_eur":round(float(obs["expected_incremental_revenue_eur"].sum(skipna=True)),2) if not obs.empty else 0.0,
        "remaining_horizon_gross_opportunity_eur":round(float(portfolio["remaining_horizon_impact_eur"].sum(skipna=True)),2) if not portfolio.empty else 0.0,
        "remaining_horizon_risk_adjusted_opportunity_eur":round(float(portfolio["risk_adjusted_horizon_impact_eur"].sum(skipna=True)),2) if not portfolio.empty else 0.0,
        "treatment_recommended_simulated_impact_eur_non_additive":round(float(tsim.loc[tsim["scenario"].eq("recommended"),"incremental_revenue"].sum()),2) if not tsim.empty else 0.0,
        "revpar_model_incremental_revenue_eur":round(float(revpar_recs["incremental_revenue_eur"].sum()),2) if not revpar_recs.empty else 0.0,
        "revpar_price_up_eur":round(float(revpar_recs.loc[revpar_recs["strategy"].eq("PRICE_UP"),"incremental_revenue_eur"].sum()),2) if not revpar_recs.empty else 0.0,
        "revpar_volume_up_eur":round(float(revpar_recs.loc[revpar_recs["strategy"].eq("PRICE_DOWN"),"incremental_revenue_eur"].sum()),2) if not revpar_recs.empty else 0.0,
        "package_price_resilience_eur_non_additive":round(float(trecs["incremental_revenue_eur"].sum()),2) if not trecs.empty else 0.0,
        "promotion_value_proxy_eur_non_additive":round(float(promotions["economic_value_proxy_eur"].sum()),2) if not promotions.empty else 0.0,
        "important_caveat":"v0.6 RevPAR and treatment recommendations use observational price-volume response proxies, not causal elasticity. Historical and treatment impacts are scenario simulations. Immediate live and remaining-horizon impacts are conditional on reconstructed pickup. Treatment impact is non-additive to room impact."
    }
    (output_dir/"summary.json").write_text(json.dumps(summary,indent=2))
    return summary
