from pathlib import Path
import pandas as pd


def fmt(df, n=None):
    if df is None or df.empty:
        return "_No rows available._"
    x = df if n is None else df.head(n)
    return x.to_markdown(index=False)


def money_format(df, columns):
    x = df.copy()
    for c in columns:
        if c in x:
            x[c] = x[c].map(lambda v: "" if pd.isna(v) else f"€{v:,.2f}")
    return x


def percent_format(df, columns):
    x = df.copy()
    for c in columns:
        if c in x:
            x[c] = x[c].map(lambda v: "" if pd.isna(v) else f"{v:.2f}%")
    return x


def ranking_section(rankings, metric, entity_col, title, unit=""):
    cols = ["rank", entity_col, "value"]
    for extra in ["observations", "reliability"]:
        if extra in rankings.columns:
            cols.append(extra)
    x = rankings[rankings.metric.eq(metric)][cols].copy()
    if x.empty:
        return ""
    if unit == "money":
        x["value"] = x.value.map(lambda v: f"€{v:,.2f}")
    elif unit == "pct":
        x["value"] = x.value.map(lambda v: f"{v:.2f}%")
    elif unit == "days":
        x["value"] = x.value.map(lambda v: f"{v:.2f}d")
    return f"### {title}\n\n{fmt(x)}\n\n"


def _safe_top(df, col, ascending=False, min_col=None, min_value=None):
    x = df.copy()
    if min_col and min_col in x and min_value is not None:
        x = x[x[min_col].ge(min_value)]
    x = x.dropna(subset=[col])
    if x.empty:
        return None
    return x.sort_values(col, ascending=ascending).iloc[0]


def executive_summary(tables):
    room = tables["room"]
    treatment = tables["treatment"]
    conv = tables["conversion_overall"].iloc[0]
    conv_room = tables.get("conversion_room_profile", pd.DataFrame())
    conv_t = tables.get("conversion_treatment_profile", pd.DataFrame())
    conv_lt = tables.get("conversion_lead_time", pd.DataFrame())

    reliable_rooms = room[room.confirmed_bookings.ge(30)]
    top_rev = _safe_top(reliable_rooms, "revenue")
    top_revpar = _safe_top(reliable_rooms, "operating_revpar")
    early = _safe_top(reliable_rooms, "avg_booking_window")
    low_canc = _safe_top(reliable_rooms, "cancellation_rate_pct", ascending=True)

    lines = ["## Executive summary\n"]
    if top_rev is not None and top_revpar is not None:
        lines.append(
            f"- **Revenue:** {top_rev.room_name} is the largest room revenue driver at €{top_rev.revenue:,.0f}, while "
            f"{top_revpar.room_name} leads reliable operating RevPAR at €{top_revpar.operating_revpar:,.0f}."
        )
    if early is not None and low_canc is not None:
        lines.append(
            f"- **Demand quality:** {early.room_name} books furthest in advance at {early.avg_booking_window:.0f} days; "
            f"{low_canc.room_name} has the lowest reliable cancellation rate at {low_canc.cancellation_rate_pct:.1f}%."
        )
    lines.append(
        f"- **Conversion:** {int(conv.requests):,} requests generated {conv.quote_rate_pct:.1f}% quotation coverage and "
        f"{conv.request_to_booking_conversion_pct:.1f}% matched request-to-booking conversion."
    )
    if not conv_room.empty:
        x = conv_room[conv_room.quoted_requests.ge(30)]
        if not x.empty:
            best = x.nlargest(1, "same_room_conversion_pct").iloc[0]
            lines.append(
                f"- **What converts:** {best.room_name} has the highest reliable same-room conversion at "
                f"{best.same_room_conversion_pct:.1f}% across {int(best.quoted_requests):,} quoted requests."
            )
    if not conv_t.empty:
        x = conv_t[
            conv_t.comparability_group.eq("COMPARABLE_COMMERCIAL")
            & conv_t.quoted_requests.ge(30)
        ]
        if not x.empty:
            best = x.nlargest(1, "same_treatment_conversion_pct").iloc[0]
            lines.append(
                f"- **Treatment conversion:** {best.arrangement_name} leads reliable same-treatment conversion at "
                f"{best.same_treatment_conversion_pct:.1f}%."
            )
    if not conv_lt.empty:
        x = conv_lt[conv_lt.requests.ge(30)]
        if not x.empty:
            best = x.nlargest(1, "conversion_pct").iloc[0]
            lines.append(
                f"- **Booking-window conversion:** the {best.booking_window_band}-day band converts best at "
                f"{best.conversion_pct:.1f}% in the reconstructed request funnel."
            )

    comparable = treatment[
        treatment.comparability_group.eq("COMPARABLE_COMMERCIAL")
        & treatment.confirmed_bookings.ge(30)
    ]
    if not comparable.empty:
        top_t = comparable.nlargest(1, "revenue").iloc[0]
        lines.append(
            f"- **Treatments:** {top_t.arrangement_name} is the largest comparable treatment revenue driver at "
            f"€{top_t.revenue:,.0f}."
        )
    lines.append(
        "- **Pricing implication:** pricing decisions should combine conversion, booking window, retained demand and occupancy; "
        "no single KPI is sufficient on its own.\n"
    )
    return "\n".join(lines) + "\n"


def conversion_section(tables):
    text = "## Conversion performance — what actually converts\n\n"
    text += (
        "> Conversion is a reconstructed **proxy** because the source does not provide a direct request-to-booking identifier. "
        "Use it directionally and comparatively, not as an audited CRM conversion rate.\n\n"
    )

    overall = tables["conversion_overall"].copy()
    text += "### Overall funnel\n\n" + fmt(percent_format(overall, [
        "quote_rate_pct", "request_to_booking_conversion_pct", "quoted_request_conversion_pct"
    ])) + "\n\n"

    room = tables.get("conversion_room_profile", pd.DataFrame()).copy()
    if not room.empty:
        cols = [
            "room_name", "quoted_requests", "overall_converted_requests", "same_room_converted_requests",
            "overall_conversion_pct", "same_room_conversion_pct", "conversion_vs_quoted_room_avg_pp",
            "avg_quote_amount", "avg_adr", "revenue", "cancellation_rate_pct",
            "operating_occupancy_pct", "operating_revpar", "conversion_reliability"
        ]
        cols = [c for c in cols if c in room]
        display = room[cols].copy()
        display = money_format(display, ["avg_quote_amount", "avg_adr", "revenue", "operating_revpar"])
        display = percent_format(display, ["overall_conversion_pct", "same_room_conversion_pct", "cancellation_rate_pct", "operating_occupancy_pct"])
        text += "### Conversion by quoted room\n\n" + fmt(display) + "\n\n"
        text += (
            "**How to read this:** `overall_conversion_pct` asks whether a request containing that quoted room converted to any booking; "
            "`same_room_conversion_pct` asks whether it converted to that same room. The second is the cleaner signal of what room solution actually converts.\n\n"
        )
        eligible = room[room.quoted_requests.ge(30)].copy()
        if not eligible.empty:
            best = eligible.nlargest(1, "same_room_conversion_pct").iloc[0]
            worst = eligible.nsmallest(1, "same_room_conversion_pct").iloc[0]
            text += "#### Room conversion insight\n\n"
            text += (
                f"- **Best reliable same-room conversion:** {best.room_name} at {best.same_room_conversion_pct:.1f}% "
                f"({int(best.quoted_requests):,} quoted requests).\n"
                f"- **Lowest reliable same-room conversion:** {worst.room_name} at {worst.same_room_conversion_pct:.1f}% "
                f"({int(worst.quoted_requests):,} quoted requests).\n"
                "- Read this together with ADR and operating RevPAR: high conversion + strong economics can support firmer pricing; "
                "low conversion should be diagnosed before increasing price.\n\n"
            )

    treatment = tables.get("conversion_treatment_profile", pd.DataFrame()).copy()
    if not treatment.empty:
        cols = [
            "arrangement_name", "comparability_group", "quoted_requests", "overall_converted_requests",
            "same_treatment_converted_requests", "overall_conversion_pct", "same_treatment_conversion_pct",
            "conversion_vs_comparable_avg_pp", "avg_quote_amount", "avg_adr", "revenue_per_booking",
            "cancellation_rate_pct", "conversion_reliability"
        ]
        cols = [c for c in cols if c in treatment]
        display = treatment[cols].copy()
        display = money_format(display, ["avg_quote_amount", "avg_adr", "revenue_per_booking"])
        display = percent_format(display, ["overall_conversion_pct", "same_treatment_conversion_pct", "cancellation_rate_pct"])
        text += "### Conversion by quoted treatment\n\n" + fmt(display) + "\n\n"
        text += (
            "Special/residence/multiproprietà treatments remain visible, but commercial treatment comparisons should focus on "
            "`COMPARABLE_COMMERCIAL` rows.\n\n"
        )

    lead = tables.get("conversion_lead_time", pd.DataFrame()).copy()
    if not lead.empty:
        lead = percent_format(lead, ["quote_rate_pct", "conversion_pct"])
        text += "### Conversion by requested booking window\n\n" + fmt(lead) + "\n\n"
        text += (
            "This table shows **when requests convert**, not only when confirmed bookings are eventually observed. "
            "It is the most useful conversion view to combine with booking pace and occupancy.\n\n"
        )

    month = tables.get("conversion_monthly", pd.DataFrame()).copy()
    if not month.empty:
        month = percent_format(month, ["quote_rate_pct", "conversion_pct"])
        text += "### Conversion by arrival month\n\n" + fmt(month) + "\n\n"

    return text



def crossover_section(tables):
    text = "## Cross-dimensional discovery — how behaviour changes\n\n"
    text += (
        "> This layer merges the dimensions Luca highlighted: **year, stay period, room, treatment, booking window, conversion, ADR/RevPAR and cancellation**. "
        "The detailed CSVs contain the full crossover population; the report shows reliable/decision-relevant slices.\n\n"
    )

    rp = tables.get("crossover_room_period", pd.DataFrame()).copy()
    if not rp.empty:
        x = rp[rp.confirmed_bookings.ge(30)].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "room_name", "confirmed_bookings",
            "avg_booking_window", "avg_adr", "occupancy_pct", "revpar", "cancellation_rate_pct", "reliability"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["room_name", "stay_month"])
        x = money_format(x, ["avg_adr", "revpar"])
        x = percent_format(x, ["occupancy_pct", "cancellation_rate_pct"])
        text += "### Room × year × season / month\n\n" + fmt(x) + "\n\n"
        text += (
            "Use this table to test whether an all-history room profile is structural. For example, an 83-day all-season booking window is only useful if it remains similar across comparable stay periods; large monthly/yearly shifts mean pricing should use period-specific lead times.\n\n"
        )

    rw = tables.get("crossover_room_period_window", pd.DataFrame()).copy()
    if not rw.empty:
        x = rw[rw.confirmed_bookings.ge(10)].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "room_name", "booking_window_band",
            "confirmed_bookings", "avg_adr", "revenue", "avg_los", "reliability"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["room_name", "stay_month", "booking_window_band"])
        x = money_format(x, ["avg_adr", "revenue"])
        text += "### Room × year × season / month × booking window\n\n" + fmt(x) + "\n\n"
        text += (
            "This is the core table for understanding **when each room is actually booked** and whether realized ADR changes as arrival approaches.\n\n"
        )

    cr = tables.get("crossover_conversion_room_period_window", pd.DataFrame()).copy()
    if not cr.empty:
        x = cr[cr.quoted_requests.ge(30)].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "room_name", "booking_window_band",
            "quoted_requests", "same_room_converted_requests", "same_room_conversion_pct",
            "overall_conversion_pct", "avg_quote_amount"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["room_name", "stay_month", "booking_window_band"])
        x = money_format(x, ["avg_quote_amount"])
        x = percent_format(x, ["same_room_conversion_pct", "overall_conversion_pct"])
        text += "### Conversion × room × year × season / month × booking window\n\n" + fmt(x) + "\n\n"
        text += (
            "This is the main demand-quality crossover: it shows whether the same room becomes more or less likely to convert at different stay periods and lead times. Only completed historical stay months are included here, so partial future 2026 periods are not treated as final.\n\n"
        )

    cw = tables.get("crossover_conversion_period_window", pd.DataFrame()).copy()
    if not cw.empty:
        x = cw[cw.requests.ge(30)].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "booking_window_band", "requests",
            "quoted_requests", "converted_requests", "quote_rate_pct", "conversion_pct"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["stay_month", "booking_window_band"])
        x = percent_format(x, ["quote_rate_pct", "conversion_pct"])
        text += "### Conversion × year × season / month × booking window\n\n" + fmt(x) + "\n\n"

    tp = tables.get("crossover_treatment_period", pd.DataFrame()).copy()
    if not tp.empty:
        x = tp[
            tp.comparability_group.eq("COMPARABLE_COMMERCIAL")
            & tp.confirmed_bookings.ge(30)
        ].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "arrangement_name", "confirmed_bookings",
            "avg_booking_window", "avg_adr", "revenue", "revenue_per_booking",
            "cancellation_rate_pct", "reliability"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["arrangement_name", "stay_month"])
        x = money_format(x, ["avg_adr", "revenue", "revenue_per_booking"])
        x = percent_format(x, ["cancellation_rate_pct"])
        text += "### Treatment × year × season / month\n\n" + fmt(x) + "\n\n"

    tw = tables.get("crossover_treatment_period_window", pd.DataFrame()).copy()
    if not tw.empty:
        x = tw[
            tw.comparability_group.eq("COMPARABLE_COMMERCIAL")
            & tw.confirmed_bookings.ge(10)
        ].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "arrangement_name", "booking_window_band",
            "confirmed_bookings", "avg_adr", "revenue", "avg_los", "reliability"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["arrangement_name", "stay_month", "booking_window_band"])
        x = money_format(x, ["avg_adr", "revenue"])
        text += "### Treatment × year × season / month × booking window\n\n" + fmt(x) + "\n\n"

    ct = tables.get("crossover_conversion_treatment_period_window", pd.DataFrame()).copy()
    if not ct.empty:
        x = ct[
            ct.comparability_group.eq("COMPARABLE_COMMERCIAL")
            & ct.quoted_requests.ge(30)
        ].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "arrangement_name", "booking_window_band",
            "quoted_requests", "same_treatment_converted_requests", "same_treatment_conversion_pct",
            "overall_conversion_pct", "avg_quote_amount"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["arrangement_name", "stay_month", "booking_window_band"])
        x = money_format(x, ["avg_quote_amount"])
        x = percent_format(x, ["same_treatment_conversion_pct", "overall_conversion_pct"])
        text += "### Conversion × treatment × year × season / month × booking window\n\n" + fmt(x) + "\n\n"

    rt = tables.get("crossover_room_treatment_period", pd.DataFrame()).copy()
    if not rt.empty:
        x = rt[
            rt.comparability_group.eq("COMPARABLE_COMMERCIAL")
            & rt.confirmed_bookings.ge(10)
        ].copy()
        cols = [
            "stay_year", "stay_month", "season_band", "room_name", "arrangement_name",
            "confirmed_bookings", "avg_adr", "revenue", "avg_booking_window", "avg_los", "reliability"
        ]
        cols = [c for c in cols if c in x]
        x = x[cols].sort_values(["room_name", "arrangement_name", "stay_month"])
        x = money_format(x, ["avg_adr", "revenue"])
        text += "### Room × treatment × year × season / month\n\n" + fmt(x) + "\n\n"

    text += (
        "**Full-population evidence:** every crossover above is also written as a dedicated `crossover_*.csv` file in the output folder, including low-volume combinations that are intentionally filtered from the readable Markdown report.\n\n"
    )
    return text

def write_report(out: Path, tables: dict[str, pd.DataFrame]):
    s = tables["scope"].iloc[0]
    p = tables["patterns"]
    text = f"""# La Casarana — Historical Pattern & Analytics MVP

## Executive scope

- **As-of date:** {s.as_of_date}
- **Completed confirmed bookings:** {int(s.completed_confirmed_bookings):,}
- **Future confirmed bookings currently on books:** {int(s.future_on_books):,}
- **Sellable physical rooms in current catalogue:** {int(s.sellable_rooms):,}
- **Excluded non-sellable/deleted/pseudo room types:** {int(s.excluded_room_types):,}

> **Design principle:** show the full population first, then reliable rankings, contextual benchmarks, conversion behaviour, distributions and interpretation.
>
> **Occupancy note:** the source does not include the hotel's historical opening calendar. The report therefore uses a clearly labelled **inferred operating-period occupancy** and does not present it as an official opening calendar.

"""
    text += executive_summary(tables)
    text += "## Decision-relevant patterns\n\n"
    for r in p.itertuples(index=False):
        text += (
            f"### {r.pattern_id} — {r.title}\n\n"
            f"**Metric:** {r.metric}  \n"
            f"**Confidence:** {r.confidence}  \n"
            f"**Evidence:** {r.evidence}  \n"
            f"**Why it matters:** {r.business_implication}\n\n"
        )

    # Conversion is intentionally early in the report because it is a core pricing signal.
    text += conversion_section(tables)

    room = tables["room"]
    room_cols = [
        "room_name", "confirmed_bookings", "revenue", "avg_adr", "avg_los",
        "avg_booking_window", "cancellation_rate_pct", "operating_occupancy_pct",
        "operating_revpar", "revenue_share_pct", "reliability"
    ]
    room_display = money_format(room[room_cols], ["revenue", "avg_adr", "operating_revpar"])
    room_display = percent_format(room_display, ["cancellation_rate_pct", "operating_occupancy_pct", "revenue_share_pct"])
    text += "## Room performance\n\n### Full room population\n\n" + fmt(room_display) + "\n\n"
    text += "Reliability: HIGH ≥100 completed confirmed bookings; MEDIUM 30–99; LOW 10–29; INSUFFICIENT <10. Rankings below require at least 30 observations.\n\n"

    rr = tables["room_rankings"]
    text += "## Reliable room rankings\n\n"
    for metric, title, unit in [
        ("avg_adr", "ADR", "money"), ("revenue", "Revenue", "money"),
        ("avg_booking_window", "Booking window", "days"),
        ("cancellation_rate_pct", "Lowest cancellation", "pct"),
        ("operating_occupancy_pct", "Inferred operating-period occupancy", "pct"),
        ("operating_revpar", "Inferred operating-period RevPAR", "money"),
        ("avg_los", "Average length of stay", "days"),
    ]:
        text += ranking_section(rr, metric, "room_name", f"Ranking by {title}", unit)

    text += "## Room comparison against meaningful benchmarks\n\n"
    text += "### Commercial performance\n\n" + fmt(money_format(tables["room_commercial_comparison"], ["revenue", "avg_adr", "operating_revpar"])) + "\n\n"
    text += "Bookings and revenue are compared with the **median room category**; ADR and RevPAR are compared with weighted property benchmarks.\n\n"
    text += "### Demand behaviour\n\n" + fmt(tables["room_demand_comparison"]) + "\n\n"
    text += "### Cancellation risk\n\n" + fmt(tables["room_risk_comparison"]) + "\n\n"
    text += "## Booking-window distribution by room\n\n" + fmt(tables["room_booking_window_distribution"]) + "\n\n"

    treatment = tables["treatment"]
    tcols = [
        "arrangement_name", "comparability_group", "confirmed_bookings", "revenue", "avg_adr",
        "avg_los", "cancellation_rate_pct", "avg_booking_window", "revenue_per_booking",
        "revenue_share_pct", "reliability"
    ]
    td = money_format(treatment[tcols], ["revenue", "avg_adr", "revenue_per_booking"])
    td = percent_format(td, ["cancellation_rate_pct", "revenue_share_pct"])
    text += "## Treatment performance\n\n### Full treatment population\n\n" + fmt(td) + "\n\n"
    text += "Only `COMPARABLE_COMMERCIAL` treatments are included in reliable treatment rankings.\n\n"
    tr = tables["treatment_rankings"]
    for metric, title, unit in [
        ("avg_adr", "ADR", "money"), ("revenue", "Revenue", "money"),
        ("avg_booking_window", "Booking window", "days"),
        ("cancellation_rate_pct", "Lowest cancellation", "pct"),
        ("avg_los", "Average length of stay", "days"),
        ("revenue_per_booking", "Revenue per booking", "money"),
    ]:
        text += ranking_section(tr, metric, "arrangement_name", f"Ranking by {title}", unit)
    text += "## Treatment comparison\n\n" + fmt(money_format(tables["treatment_comparison"], ["revenue", "avg_adr", "revenue_per_booking"])) + "\n\n"
    text += "## Booking-window distribution by treatment\n\n" + fmt(tables["treatment_booking_window_distribution"]) + "\n\n"

    occ_cols = [
        "stay_month", "occupied_room_nights", "calendar_available_room_nights", "calendar_occupancy_pct",
        "inferred_operating_month", "operating_occupancy_pct", "peak_daily_room_type_occupancy_pct", "over_capacity_rows"
    ]
    text += "## Occupancy by completed stay month\n\n" + fmt(tables["occupancy_monthly"][occ_cols]) + "\n\n"
    text += "## Property booking-window distribution\n\n" + fmt(tables["booking_window"]) + "\n\n"

    # Luca's requested Layer-3 discovery: merge room/treatment, seasonality,
    # booking window, conversion, ADR/RevPAR and year-over-year context.
    text += crossover_section(tables)

    text += "## Data-quality checks\n\n" + fmt(tables["validation"]) + "\n\n"
    text += """## Methodology and limits

- **Operating period:** inferred from months with meaningful occupied inventory. It is not an official opening calendar.
- **Room occupancy:** current catalogue capacity is applied historically. Room reassignment and historical capacity changes can create room-type/date values above 100%; these are flagged, not clipped.
- **Treatment comparability:** standard commercial board/rate plans are ranked together. Residence, multiproprietà and special categories remain visible but are excluded from directly comparable rankings.
- **Reliability:** full-population tables include every category. Reliable rankings generally require at least 30 observations.
- **Conversion:** request-to-booking conversion is reconstructed one-to-one because the source has no direct request-to-booking identifier. Room/treatment conversion therefore remains a proxy and should be used comparatively.
- **Same-room / same-treatment conversion:** these metrics measure whether a request containing a quoted solution ultimately matched to a booking of that same solution; they are more specific than overall request conversion.
- **Causality:** differences describe historical associations, not price elasticity or causal impact.
- **Cross-year comparison:** historical crossover tables use completed stay periods for bookings and completed stay months for conversion; incomplete future stay months are not treated as final YoY performance.
- **Live pickup:** a single extraction supports historical distributions; recurring snapshots are required for reliable acceleration/deceleration signals.
"""
    (out / "pattern_report.md").write_text(text, encoding="utf-8")
