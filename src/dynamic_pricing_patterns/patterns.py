import pandas as pd


def detect_patterns(
    monthly, room, treatment, occ_monthly, conv, pace,
    conversion_room=None, conversion_treatment=None, conversion_lead_time=None,
):
    rows = []

    def add(pid, title, metric, evidence, implication, confidence):
        rows.append({
            "pattern_id": pid,
            "title": title,
            "metric": metric,
            "confidence": confidence,
            "evidence": evidence,
            "business_implication": implication,
        })

    operating = occ_monthly[occ_monthly.inferred_operating_month].copy()
    if len(operating) >= 4:
        hi = operating.nlargest(3, "operating_occupancy_pct")
        lo = operating.nsmallest(3, "operating_occupancy_pct")
        add(
            "P01", "Demand is strongly seasonal during inferred operating periods", "operating-period occupancy",
            f"The strongest operating months are {', '.join(hi.stay_month)} "
            f"({', '.join(f'{x:.1f}%' for x in hi.operating_occupancy_pct)}); "
            f"the weakest active months are {', '.join(lo.stay_month)}.",
            "Use separate high-season yield and shoulder-season volume strategies; do not treat closed months as zero-demand inventory.",
            "HIGH",
        )

    eligible = room[room.confirmed_bookings.ge(30)].copy()
    if len(eligible) >= 2:
        top_rev = eligible.nlargest(1, "revenue").iloc[0]
        observed_top_adr = room.nlargest(1, "avg_adr").iloc[0]
        reliable_top_adr = eligible.nlargest(1, "avg_adr").iloc[0]
        early = eligible.nlargest(1, "avg_booking_window").iloc[0]
        low_canc = eligible.nsmallest(1, "cancellation_rate_pct").iloc[0]
        best_revpar = eligible.nlargest(1, "operating_revpar").iloc[0]
        property_bw = (eligible.avg_booking_window * eligible.confirmed_bookings).sum() / eligible.confirmed_bookings.sum()
        property_canc = eligible.canceled_bookings.sum() / eligible.total_bookings.sum() * 100

        add(
            "P02", "Revenue scale and pricing power sit in different rooms", "room commercial profile",
            f"{top_rev.room_name} leads reliable room revenue at €{top_rev.revenue:,.0f}, while {best_revpar.room_name} "
            f"leads operating RevPAR at €{best_revpar.operating_revpar:,.0f}. The highest observed ADR is "
            f"{observed_top_adr.room_name} at €{observed_top_adr.avg_adr:,.0f} ({int(observed_top_adr.confirmed_bookings)} bookings); "
            f"the highest reliable ADR is {reliable_top_adr.room_name} at €{reliable_top_adr.avg_adr:,.0f}.",
            "Use total revenue to understand scale, and ADR/RevPAR to understand pricing power and inventory productivity.",
            "HIGH",
        )
        add(
            "P03", "Early-booking demand is concentrated and more predictable in the strongest lead-time room", "booking window + cancellation",
            f"{early.room_name} books {early.avg_booking_window:.0f} days ahead versus a reliable-room weighted average of "
            f"{property_bw:.0f} days, with cancellation {early.cancellation_rate_pct:.1f}% versus {property_canc:.1f}%.",
            "Review pricing earlier for rooms that combine long lead time with lower cancellation risk.",
            "HIGH",
        )
        add(
            "P04", "Cancellation changes the quality of apparent demand", "cancellation risk",
            f"{low_canc.room_name} has the lowest reliable cancellation rate at {low_canc.cancellation_rate_pct:.1f}%, "
            f"{property_canc-low_canc.cancellation_rate_pct:.1f} percentage points below the reliable-room average.",
            "Use retained demand, not gross bookings alone, when interpreting saturation and pickup.",
            "HIGH",
        )

    comparable = treatment[
        treatment.comparability_group.eq("COMPARABLE_COMMERCIAL")
        & treatment.confirmed_bookings.ge(30)
    ].copy()
    if len(comparable) >= 2:
        top2 = comparable.nlargest(2, "revenue")
        a, b = top2.iloc[0], top2.iloc[1]
        concentration = top2.revenue.sum() / comparable.revenue.sum() * 100
        add(
            "P05", "Commercial treatment economics are concentrated", "treatment concentration",
            f"{a.arrangement_name} and {b.arrangement_name} generate {concentration:.1f}% of comparable treatment revenue. "
            f"{a.arrangement_name} ADR is €{a.avg_adr:,.0f} versus €{b.avg_adr:,.0f}, with cancellation "
            f"{a.cancellation_rate_pct:.1f}% versus {b.cancellation_rate_pct:.1f}%.",
            "Prioritize pricing and conversion tests on treatments that combine meaningful volume with strong economics.",
            "HIGH",
        )

    if conversion_room is not None and not conversion_room.empty:
        eligible_conv = conversion_room[conversion_room.quoted_requests.ge(30)].copy()
        if not eligible_conv.empty:
            best = eligible_conv.nlargest(1, "same_room_conversion_pct").iloc[0]
            worst = eligible_conv.nsmallest(1, "same_room_conversion_pct").iloc[0]
            add(
                "P06", "Room conversion varies materially across quoted solutions", "same-room conversion",
                f"Among rooms with 30+ quoted requests, {best.room_name} converts {best.same_room_conversion_pct:.1f}% of quoted requests "
                f"to the same room, versus {worst.room_name} at {worst.same_room_conversion_pct:.1f}%.",
                "Treat room-level conversion as a demand-quality signal: high conversion can support firmer pricing, while low conversion needs diagnosis before price increases.",
                "MEDIUM",
            )
            high_value = eligible_conv.dropna(subset=["avg_adr"]).sort_values(
                ["same_room_conversion_pct", "avg_adr"], ascending=[False, False]
            ).iloc[0]
            add(
                "P07", "Some rooms combine conversion with premium economics", "conversion + ADR",
                f"{high_value.room_name} combines same-room conversion of {high_value.same_room_conversion_pct:.1f}% with ADR €{high_value.avg_adr:,.0f} "
                f"and operating RevPAR €{high_value.operating_revpar:,.0f}.",
                "Rooms that sustain both conversion and premium economics are the strongest candidates for protecting or cautiously increasing price.",
                "MEDIUM",
            )

    if conversion_treatment is not None and not conversion_treatment.empty:
        x = conversion_treatment[
            conversion_treatment.comparability_group.eq("COMPARABLE_COMMERCIAL")
            & conversion_treatment.quoted_requests.ge(30)
        ].copy()
        if not x.empty:
            best = x.nlargest(1, "same_treatment_conversion_pct").iloc[0]
            add(
                "P08", "Treatment demand differs in actual conversion, not only revenue", "same-treatment conversion",
                f"{best.arrangement_name} has the highest reliable same-treatment conversion at {best.same_treatment_conversion_pct:.1f}% "
                f"across {int(best.quoted_requests)} quoted requests.",
                "Use treatment conversion together with ADR and revenue per booking to distinguish popular offers from merely high-volume offers.",
                "MEDIUM",
            )

    if conversion_lead_time is not None and not conversion_lead_time.empty:
        eligible_lt = conversion_lead_time[conversion_lead_time.requests.ge(30)].copy()
        if len(eligible_lt) >= 2:
            best = eligible_lt.nlargest(1, "conversion_pct").iloc[0]
            worst = eligible_lt.nsmallest(1, "conversion_pct").iloc[0]
            add(
                "P09", "Conversion changes with booking window", "lead-time conversion",
                f"The highest-converting lead-time band is {best.booking_window_band} days at {best.conversion_pct:.1f}%, "
                f"versus {worst.booking_window_band} days at {worst.conversion_pct:.1f}%.",
                "Use lead-time conversion with occupancy and booking pace when deciding whether to push price or protect volume.",
                "MEDIUM",
            )

    if not conv.empty:
        x = conv.iloc[0]
        add(
            "P10", "The funnel loses most demand after quotation", "request conversion",
            f"Of {int(x.requests):,} requests, {x.quote_rate_pct:.1f}% receive a quote but only "
            f"{x.request_to_booking_conversion_pct:.1f}% are matched to confirmed bookings.",
            "Conversion deserves the same monitoring priority as occupancy and booking window; however, the request-to-booking link remains a proxy.",
            "MEDIUM",
        )

    if not monthly.empty:
        cm = monthly[monthly.bookings_total.ge(30)].nlargest(1, "cancellation_rate_pct")
        if not cm.empty:
            x = cm.iloc[0]
            add(
                "P11", "Cancellation risk peaks in a core arrival month", "monthly cancellation",
                f"The highest cancellation rate among months with 30+ bookings is {x.arrival_month} at {x.cancellation_rate_pct:.1f}%.",
                "Discount gross demand by month-specific cancellation risk before using it as a pricing trigger.",
                "HIGH",
            )

    if not pace.empty:
        vals = pace[[c for c in pace if c.startswith("booked_by_")]].mean()
        add(
            "P12", "Historical booking pace is a baseline, not yet a live signal", "booking pace",
            f"Average completed-stay booking shares range from {vals.min():.1f}% to {vals.max():.1f}% across lead-time checkpoints.",
            "Store recurring snapshots before interpreting deviations as acceleration or slowdown.",
            "MEDIUM",
        )

    anomalies = int(occ_monthly.over_capacity_rows.sum())
    if anomalies:
        add(
            "P13", "Room-category occupancy contains capacity conflicts", "data quality",
            f"The historical reconstruction contains {anomalies} room-type/date rows above current catalogue capacity.",
            "Treat property-level occupancy as more reliable than room-category occupancy until historical capacity and reassignment logic are confirmed.",
            "HIGH",
        )

    return pd.DataFrame(rows)


def detect_crossover_patterns(room_period, room_window, treatment_period, conversion_room, conversion_treatment):
    """Evidence-led Layer-3 patterns from cross-dimensional tables."""
    rows = []

    def add(pid, title, metric, evidence, implication, confidence="MEDIUM"):
        rows.append({
            "pattern_id": pid,
            "title": title,
            "metric": metric,
            "confidence": confidence,
            "evidence": evidence,
            "business_implication": implication,
        })

    rp = room_period[room_period.confirmed_bookings.ge(30)].copy()
    if not rp.empty:
        spread = rp.groupby("room_name").avg_booking_window.agg(["min", "max", "count"]).reset_index()
        spread = spread[spread["count"].ge(2)]
        if not spread.empty:
            spread["delta"] = spread["max"] - spread["min"]
            x = spread.nlargest(1, "delta").iloc[0]
            add(
                "X01",
                "Aggregate room booking windows hide large seasonal shifts",
                "room × year × season × booking window",
                f"{x.room_name} has a {x.delta:.0f}-day spread between its shortest and longest reliable monthly booking-window averages.",
                "Use room-and-period-specific lead-time curves instead of one all-season room average when deciding how early pricing should react.",
                "HIGH",
            )

        rev = rp.dropna(subset=["revpar"])
        if not rev.empty:
            x = rev.nlargest(1, "revpar").iloc[0]
            add(
                "X02",
                "Room RevPAR leadership changes by stay period",
                "room × year × season × RevPAR",
                f"The strongest reliable room-month RevPAR is {x.room_name} in {x.stay_month} at €{x.revpar:,.0f}.",
                "Monitor room productivity by stay period; an all-season RevPAR average can hide where pricing power is strongest.",
                "HIGH",
            )

    cr = conversion_room[conversion_room.quoted_requests.ge(30)].copy()
    if not cr.empty:
        x = cr.nlargest(1, "same_room_conversion_pct").iloc[0]
        add(
            "X03",
            "Room conversion depends on both stay period and booking window",
            "conversion × room × year × season × booking window",
            f"The strongest sufficiently observed same-room conversion is {x.room_name}, {x.stay_month}, {x.booking_window_band}: {x.same_room_conversion_pct:.1f}% across {int(x.quoted_requests)} quoted requests.",
            "Read conversion in its room, stay-period and lead-time context before treating it as upward or downward pricing pressure.",
            "MEDIUM",
        )

    tp = treatment_period[
        treatment_period.comparability_group.eq("COMPARABLE_COMMERCIAL")
        & treatment_period.confirmed_bookings.ge(30)
    ].copy()
    if not tp.empty:
        spread = tp.groupby("arrangement_name").avg_booking_window.agg(["min", "max", "count"]).reset_index()
        spread = spread[spread["count"].ge(2)]
        if not spread.empty:
            spread["delta"] = spread["max"] - spread["min"]
            x = spread.nlargest(1, "delta").iloc[0]
            add(
                "X04",
                "Treatment booking behaviour changes through the season",
                "treatment × year × season × booking window",
                f"{x.arrangement_name} has a {x.delta:.0f}-day spread between its shortest and longest reliable monthly booking-window averages.",
                "Evaluate treatment pricing and demand by stay period rather than relying on one all-season treatment average.",
                "MEDIUM",
            )

    ct = conversion_treatment[
        conversion_treatment.quoted_requests.ge(30)
        & conversion_treatment.comparability_group.eq("COMPARABLE_COMMERCIAL")
    ].copy()
    if not ct.empty:
        x = ct.nlargest(1, "same_treatment_conversion_pct").iloc[0]
        add(
            "X05",
            "Treatment acceptance changes by season and booking window",
            "conversion × treatment × year × season × booking window",
            f"The strongest sufficiently observed same-treatment conversion is {x.arrangement_name}, {x.stay_month}, {x.booking_window_band}: {x.same_treatment_conversion_pct:.1f}% across {int(x.quoted_requests)} quoted requests.",
            "Validate treatment price and packaging in the specific stay-period and booking-window context where customers actually accept it.",
            "MEDIUM",
        )

    return pd.DataFrame(rows)
