from pathlib import Path
from .config import AnalysisConfig
from .loaders import load_all, infer_as_of
from .validation import validate_inputs
from .analytics import (
    dataset_overview,
    scope_summary,
    booking_window_summary,
    monthly_performance,
    room_performance,
    treatment_performance,
    occupancy_daily,
    occupancy_monthly,
    apply_operating_occupancy_to_rooms,
    conversion_analytics,
    booking_pace,
    build_comparison_profiles,
    room_booking_window_distribution,
    treatment_booking_window_distribution,
    enrich_conversion_profiles,
    room_time_crossovers,
    treatment_time_crossovers,
    room_treatment_crossovers,
    conversion_crossovers,
)
from .patterns import detect_patterns, detect_crossover_patterns
from .report import write_report


def _clear(out):
    out.mkdir(parents=True, exist_ok=True)
    for pat in ("*.csv", "*.md"):
        for p in out.glob(pat):
            p.unlink()


def run_pipeline(data_dir: Path, output_dir: Path, config: AnalysisConfig | None = None):
    cfg = config or AnalysisConfig()
    _clear(output_dir)
    data = load_all(data_dir)
    as_of = infer_as_of(data)
    validation = validate_inputs(data)
    b = data["fact_prenotazioni"]
    rooms = data["dim_camere"]

    tables = {
        "validation": validation.checks,
        "overview": dataset_overview(data),
        "scope": scope_summary(b, rooms, as_of, cfg),
        "booking_window": booking_window_summary(b, as_of, cfg),
        "monthly": monthly_performance(b, as_of, cfg),
        "treatment": treatment_performance(b, as_of, cfg),
    }
    tables["occupancy_daily"] = occupancy_daily(b, rooms, as_of, cfg)
    tables["occupancy_monthly"] = occupancy_monthly(tables["occupancy_daily"], cfg)
    tables["room"] = room_performance(b, rooms, as_of, cfg, tables["occupancy_daily"])
    tables["room"] = apply_operating_occupancy_to_rooms(tables["room"], tables["occupancy_daily"], tables["occupancy_monthly"])
    tables["room_booking_window_distribution"] = room_booking_window_distribution(b, as_of, cfg)
    tables["treatment_booking_window_distribution"] = treatment_booking_window_distribution(b, as_of, cfg)
    tables.update(build_comparison_profiles(tables["room"], tables["treatment"], cfg))

    overall, monthly, room_conv, treatment_conv, lead_time_conv, matches = conversion_analytics(
        data["fact_richieste"], data["fact_richieste_preventivi"], b, cfg
    )
    conversion_room_profile, conversion_treatment_profile = enrich_conversion_profiles(
        room_conv, treatment_conv, tables["room"], tables["treatment"], cfg
    )
    tables.update({
        "conversion_overall": overall,
        "conversion_monthly": monthly,
        "conversion_room": room_conv,
        "conversion_treatment": treatment_conv,
        "conversion_lead_time": lead_time_conv,
        "conversion_room_profile": conversion_room_profile,
        "conversion_treatment_profile": conversion_treatment_profile,
        "request_booking_matches": matches,
        "booking_pace": booking_pace(b, as_of, cfg),
    })
    room_period, room_period_window = room_time_crossovers(
        b, tables["occupancy_daily"], as_of, cfg
    )
    treatment_period, treatment_period_window = treatment_time_crossovers(b, as_of, cfg)
    conversion_period_window, conversion_room_period_window, conversion_treatment_period_window = conversion_crossovers(
        data["fact_richieste"], data["fact_richieste_preventivi"], b, as_of, cfg
    )
    tables.update({
        "crossover_room_period": room_period,
        "crossover_room_period_window": room_period_window,
        "crossover_treatment_period": treatment_period,
        "crossover_treatment_period_window": treatment_period_window,
        "crossover_room_treatment_period": room_treatment_crossovers(b, as_of, cfg),
        "crossover_conversion_period_window": conversion_period_window,
        "crossover_conversion_room_period_window": conversion_room_period_window,
        "crossover_conversion_treatment_period_window": conversion_treatment_period_window,
    })

    tables["patterns"] = detect_patterns(
        tables["monthly"],
        tables["room"],
        tables["treatment"],
        tables["occupancy_monthly"],
        overall,
        tables["booking_pace"],
        tables["conversion_room_profile"],
        tables["conversion_treatment_profile"],
        tables["conversion_lead_time"],
    )
    cross_patterns = detect_crossover_patterns(
        tables["crossover_room_period"],
        tables["crossover_room_period_window"],
        tables["crossover_treatment_period"],
        tables["crossover_conversion_room_period_window"],
        tables["crossover_conversion_treatment_period_window"],
    )
    if not cross_patterns.empty:
        import pandas as pd
        tables["patterns"] = pd.concat([tables["patterns"], cross_patterns], ignore_index=True)

    for name, dataframe in tables.items():
        dataframe.to_csv(output_dir / f"{name}.csv", index=False)
    write_report(output_dir, tables)
    return tables
