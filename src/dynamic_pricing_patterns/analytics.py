from __future__ import annotations
import numpy as np
import pandas as pd
from .config import AnalysisConfig


def reliability_label(n: float, cfg: AnalysisConfig) -> str:
    if n >= cfg.reliability_high_min:
        return "HIGH"
    if n >= cfg.reliability_medium_min:
        return "MEDIUM"
    if n >= cfg.reliability_low_min:
        return "LOW"
    return "INSUFFICIENT"


def classify_treatment(code: object, cfg: AnalysisConfig) -> str:
    value = "" if pd.isna(code) else str(code).upper().strip()
    if value in cfg.comparable_treatment_codes:
        return "COMPARABLE_COMMERCIAL"
    if value in cfg.special_treatment_codes:
        return "SPECIAL_OR_NON_COMPARABLE"
    return "UNCLASSIFIED"


def confirmed_bookings(df, cfg):
    return df[df.status.isin(cfg.confirmed_statuses)].copy()


def canceled_bookings(df, cfg):
    return df[df.status.isin(cfg.canceled_statuses)].copy()


def sellable_rooms(rooms: pd.DataFrame, cfg: AnalysisConfig) -> pd.DataFrame:
    x = rooms[(rooms.deleted.eq(0)) & (rooms.quantity.gt(0))].copy()
    bad = x.name.fillna("").str.upper().apply(
        lambda n: n.strip() == "-" or any(t in n for t in cfg.pseudo_room_tokens)
    )
    return x[~bad].copy()


def dataset_overview(data):
    rows = []
    for name, df in data.items():
        dates = []
        for c in [c for c in df if "date" in c or "datetime" in c]:
            s = pd.to_datetime(df[c], errors="coerce").dropna()
            if not s.empty:
                dates.extend([s.min(), s.max()])
        rows.append({
            "dataset": name,
            "rows": len(df),
            "columns": len(df.columns),
            "date_min": min(dates).date().isoformat() if dates else "",
            "date_max": max(dates).date().isoformat() if dates else "",
            "missing_cells_pct": round(df.isna().mean().mean() * 100, 2),
        })
    return pd.DataFrame(rows)


def scope_summary(bookings, rooms, as_of, cfg):
    completed = confirmed_bookings(bookings, cfg)
    completed = completed[completed.checkout_date.le(as_of)]
    future = confirmed_bookings(bookings, cfg)
    future = future[future.checkin_date.gt(as_of)]
    sr = sellable_rooms(rooms, cfg)
    return pd.DataFrame([{
        "as_of_date": as_of.date().isoformat(),
        "completed_confirmed_bookings": completed.booking_code.nunique(),
        "future_on_books": future.booking_code.nunique(),
        "sellable_room_types": len(sr),
        "sellable_rooms": int(sr.quantity.sum()),
        "excluded_room_types": len(rooms) - len(sr),
    }])


def booking_window_summary(bookings, as_of, cfg):
    b = confirmed_bookings(bookings, cfg)
    b = b[b.checkout_date.le(as_of) & b.lead_time_days.ge(0)].copy()
    b["booking_window_band"] = pd.cut(
        b.lead_time_days,
        bins=cfg.booking_window_bins,
        labels=cfg.booking_window_labels,
    )
    out = b.groupby("booking_window_band", observed=True).agg(
        bookings=("booking_code", "nunique"),
        room_nights=("nights", "sum"),
        revenue=("total_stay_amount", "sum"),
        adr=("adr", "mean"),
    ).reset_index()
    out["booking_share_pct"] = (out.bookings / out.bookings.sum() * 100).round(2)
    return out.round(2)


def monthly_performance(bookings, as_of, cfg):
    b = bookings[bookings.checkout_date.le(as_of)].copy()
    b["arrival_month"] = b.checkin_date.dt.to_period("M").astype(str)
    rows = []
    for month, g in b.groupby("arrival_month"):
        conf = confirmed_bookings(g, cfg)
        canc = canceled_bookings(g, cfg)
        rows.append({
            "arrival_month": month,
            "bookings_total": g.booking_code.nunique(),
            "confirmed_bookings": conf.booking_code.nunique(),
            "canceled_bookings": canc.booking_code.nunique(),
            "pending_bookings": int(g.status.isin(cfg.pending_statuses).sum()),
            "confirmed_revenue": conf.total_stay_amount.sum(),
            "avg_adr": conf.adr.mean(),
            "avg_booking_window": conf.loc[conf.lead_time_days.ge(0), "lead_time_days"].mean(),
            "cancellation_rate_pct": canc.booking_code.nunique() / g.booking_code.nunique() * 100 if len(g) else np.nan,
        })
    return pd.DataFrame(rows).round(2)


def room_performance(bookings, rooms, as_of, cfg, occ_daily=None):
    b = bookings[bookings.checkout_date.le(as_of)].copy()
    c = confirmed_bookings(b, cfg)
    base = c.groupby(["room_id", "room_name"]).agg(
        confirmed_bookings=("booking_code", "nunique"),
        room_nights=("nights", "sum"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
        revenue_per_booking=("total_stay_amount", "mean"),
    ).reset_index()
    total = b.groupby("room_id").booking_code.nunique().rename("total_bookings")
    canc = canceled_bookings(b, cfg).groupby("room_id").booking_code.nunique().rename("canceled_bookings")
    out = base.merge(total, on="room_id", how="left").merge(canc, on="room_id", how="left")
    out = out.merge(rooms[["id", "quantity", "deleted"]], left_on="room_id", right_on="id", how="left")
    out["canceled_bookings"] = out.canceled_bookings.fillna(0)
    out["cancellation_rate_pct"] = out.canceled_bookings / out.total_bookings * 100
    if occ_daily is not None and not occ_daily.empty:
        occ = occ_daily.groupby(["room_id", "room_name"]).agg(
            occupied_room_nights=("occupied_rooms", "sum"),
            available_room_nights=("capacity", "sum"),
        ).reset_index()
        occ["occupancy_pct"] = occ.occupied_room_nights / occ.available_room_nights * 100
        out = out.merge(occ[["room_id", "occupancy_pct"]], on="room_id", how="left")
    else:
        out["occupancy_pct"] = np.nan
    out["revpar"] = out.avg_adr * out.occupancy_pct / 100
    out["revenue_share_pct"] = out.revenue / out.revenue.sum() * 100
    out["reliability"] = out.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))
    return out.drop(columns="id").sort_values("revenue", ascending=False).round(2)

def treatment_performance(bookings, as_of, cfg):
    b = bookings[bookings.checkout_date.le(as_of)].copy()
    c = confirmed_bookings(b, cfg)
    base = c.groupby(["arrangement_code", "arrangement_name"], dropna=False).agg(
        confirmed_bookings=("booking_code", "nunique"),
        room_nights=("nights", "sum"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
        revenue_per_booking=("total_stay_amount", "mean"),
    ).reset_index()
    total = b.groupby("arrangement_code", dropna=False).booking_code.nunique().rename("total_bookings")
    canc = canceled_bookings(b, cfg).groupby("arrangement_code", dropna=False).booking_code.nunique().rename("canceled_bookings")
    out = base.merge(total, on="arrangement_code", how="left").merge(canc, on="arrangement_code", how="left")
    out["canceled_bookings"] = out.canceled_bookings.fillna(0)
    out["cancellation_rate_pct"] = out.canceled_bookings / out.total_bookings * 100
    out["revenue_share_pct"] = out.revenue / out.revenue.sum() * 100
    out["comparability_group"] = out.arrangement_code.apply(lambda c: classify_treatment(c, cfg))
    out["reliability"] = out.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))
    return out.sort_values("revenue", ascending=False).round(2)

def occupancy_daily(bookings, rooms, as_of, cfg):
    sr = sellable_rooms(rooms, cfg)
    b = confirmed_bookings(bookings, cfg)
    b = b[b.checkin_date.lt(as_of) & b.room_id.isin(sr.id)]
    start = max(b.checkin_date.min().normalize(), pd.Timestamp("2024-01-01"))
    end = min(as_of, b.checkout_date.max()).normalize() - pd.Timedelta(days=1)
    grid = pd.MultiIndex.from_product(
        [pd.date_range(start, end), sr.id], names=["stay_date", "room_id"]
    ).to_frame(index=False)
    grid = grid.merge(sr[["id", "name", "quantity"]], left_on="room_id", right_on="id", how="left")
    grid = grid.drop(columns="id").rename(columns={"name": "room_name", "quantity": "capacity"})
    rows = []
    for r in b.itertuples(index=False):
        last = min(r.checkout_date.normalize(), as_of)
        for d in pd.date_range(r.checkin_date.normalize(), last - pd.Timedelta(days=1)):
            rows.append((d, r.room_id, r.booking_code))
    if rows:
        occ = pd.DataFrame(rows, columns=["stay_date", "room_id", "booking_code"])
        occ = occ.groupby(["stay_date", "room_id"]).booking_code.nunique().rename("occupied_rooms").reset_index()
    else:
        occ = pd.DataFrame(columns=["stay_date", "room_id", "occupied_rooms"])
    out = grid.merge(occ, on=["stay_date", "room_id"], how="left")
    out.occupied_rooms = out.occupied_rooms.fillna(0).astype(int)
    out["occupancy_pct"] = out.occupied_rooms / out.capacity * 100
    out["over_capacity_flag"] = out.occupied_rooms.gt(out.capacity)
    return out.round(2)


def occupancy_monthly(occ, cfg: AnalysisConfig):
    x = occ.copy()
    x["stay_month"] = x.stay_date.dt.to_period("M").astype(str)
    rows = []
    for m, g in x.groupby("stay_month"):
        occupied = g.occupied_rooms.sum()
        available = g.capacity.sum()
        calendar_occ = occupied / available * 100 if available else np.nan
        rows.append({
            "stay_month": m,
            "occupied_room_nights": occupied,
            "calendar_available_room_nights": available,
            "calendar_occupancy_pct": calendar_occ,
            "peak_daily_room_type_occupancy_pct": g.occupancy_pct.max(),
            "over_capacity_rows": int(g.over_capacity_flag.sum()),
        })
    out = pd.DataFrame(rows)
    out["inferred_operating_month"] = (
        out.occupied_room_nights.ge(cfg.operating_month_min_occupied_room_nights)
        & out.calendar_occupancy_pct.ge(cfg.operating_month_min_calendar_occupancy_pct)
    )
    out["operating_available_room_nights"] = np.where(
        out.inferred_operating_month, out.calendar_available_room_nights, 0
    )
    out["operating_occupancy_pct"] = np.where(
        out.inferred_operating_month, out.calendar_occupancy_pct, np.nan
    )
    return out.round(2)


def apply_operating_occupancy_to_rooms(room, occ_daily, occ_monthly):
    active_months = set(occ_monthly.loc[occ_monthly.inferred_operating_month, "stay_month"])
    x = occ_daily.copy()
    x["stay_month"] = x.stay_date.dt.to_period("M").astype(str)
    active = x[x.stay_month.isin(active_months)]
    if active.empty:
        room["operating_occupancy_pct"] = np.nan
        room["operating_revpar"] = np.nan
        return room
    agg = active.groupby("room_id").agg(
        operating_occupied_room_nights=("occupied_rooms", "sum"),
        operating_available_room_nights=("capacity", "sum"),
    ).reset_index()
    agg["operating_occupancy_pct"] = (
        agg.operating_occupied_room_nights / agg.operating_available_room_nights * 100
    )
    out = room.merge(agg, on="room_id", how="left")
    out["operating_revpar"] = out.avg_adr * out.operating_occupancy_pct / 100
    return out.round(2)


def match_requests_to_bookings(requests, bookings, cfg):
    r = requests.sort_values("creation_datetime").copy()
    b = confirmed_bookings(bookings, cfg).sort_values("creation_datetime").copy()
    candidates = r.merge(
        b[["booking_code", "customer_code", "checkin_date", "creation_datetime", "room_id", "arrangement_code"]],
        on=["customer_code", "checkin_date"],
        suffixes=("_request", "_booking"),
        how="left",
    )
    candidates["lag_days"] = (
        candidates.creation_datetime_booking - candidates.creation_datetime_request
    ).dt.total_seconds() / 86400
    candidates = candidates[candidates.lag_days.between(0, cfg.conversion_match_max_days, inclusive="both")]
    candidates = candidates.sort_values(["booking_code", "lag_days"]).drop_duplicates("booking_code", keep="first")
    matched = candidates[["request_code", "booking_code", "room_id", "arrangement_code_booking"]].rename(
        columns={"room_id": "booked_room_id", "arrangement_code_booking": "booked_arrangement_code"}
    )
    return r.merge(matched, on="request_code", how="left").assign(
        converted=lambda x: x.booking_code.notna().astype(int)
    )


def conversion_analytics(requests, quotes, bookings, cfg):
    r = match_requests_to_bookings(requests, bookings, cfg)
    overall = pd.DataFrame([{
        "requests": r.request_code.nunique(),
        "requests_with_quote": r.loc[r.has_quotation.eq(1), "request_code"].nunique(),
        "quote_rate_pct": r.has_quotation.mean() * 100,
        "converted_requests": r.loc[r.converted.eq(1), "request_code"].nunique(),
        "request_to_booking_conversion_pct": r.converted.mean() * 100,
        "quoted_request_conversion_pct": r.loc[r.has_quotation.eq(1), "converted"].mean() * 100,
    }]).round(2)

    r["arrival_month"] = r.checkin_date.dt.to_period("M").astype(str)
    r["booking_window_band"] = pd.cut(
        r.lead_time_days, bins=cfg.booking_window_bins, labels=cfg.booking_window_labels
    )

    by_month = r.groupby("arrival_month").agg(
        requests=("request_code", "nunique"),
        quoted_requests=("has_quotation", "sum"),
        converted_requests=("converted", "sum"),
        quote_rate_pct=("has_quotation", "mean"),
        conversion_pct=("converted", "mean"),
        avg_requested_lead_time=("lead_time_days", "mean"),
    ).reset_index()
    by_month[["quote_rate_pct", "conversion_pct"]] *= 100

    by_lead_time = r.groupby("booking_window_band", observed=True).agg(
        requests=("request_code", "nunique"),
        quoted_requests=("has_quotation", "sum"),
        converted_requests=("converted", "sum"),
        quote_rate_pct=("has_quotation", "mean"),
        conversion_pct=("converted", "mean"),
    ).reset_index()
    by_lead_time[["quote_rate_pct", "conversion_pct"]] *= 100

    q = quotes.merge(
        r[["request_code", "converted", "booked_room_id", "booked_arrangement_code"]],
        on="request_code", how="inner"
    )

    qr = q.groupby(["request_code", "room_id", "room_name"], as_index=False).agg(
        avg_quote_amount=("total_amount", "mean"),
        converted=("converted", "max"),
        booked_room_id=("booked_room_id", "first"),
    )
    qr["same_room_conversion"] = (qr.converted.eq(1) & qr.room_id.eq(qr.booked_room_id)).astype(int)
    by_room = qr.groupby(["room_id", "room_name"]).agg(
        quoted_requests=("request_code", "nunique"),
        overall_converted_requests=("converted", "sum"),
        same_room_converted_requests=("same_room_conversion", "sum"),
        avg_quote_amount=("avg_quote_amount", "mean"),
    ).reset_index()
    by_room["overall_conversion_pct"] = by_room.overall_converted_requests / by_room.quoted_requests * 100
    by_room["same_room_conversion_pct"] = by_room.same_room_converted_requests / by_room.quoted_requests * 100

    qt = q.groupby(["request_code", "arrangement_code", "arrangement_name"], dropna=False, as_index=False).agg(
        avg_quote_amount=("total_amount", "mean"),
        converted=("converted", "max"),
        booked_arrangement_code=("booked_arrangement_code", "first"),
    )
    qt["same_treatment_conversion"] = (
        qt.converted.eq(1) & qt.arrangement_code.eq(qt.booked_arrangement_code)
    ).astype(int)
    by_t = qt.groupby(["arrangement_code", "arrangement_name"], dropna=False).agg(
        quoted_requests=("request_code", "nunique"),
        overall_converted_requests=("converted", "sum"),
        same_treatment_converted_requests=("same_treatment_conversion", "sum"),
        avg_quote_amount=("avg_quote_amount", "mean"),
    ).reset_index()
    by_t["overall_conversion_pct"] = by_t.overall_converted_requests / by_t.quoted_requests * 100
    by_t["same_treatment_conversion_pct"] = by_t.same_treatment_converted_requests / by_t.quoted_requests * 100

    return (
        overall, by_month.round(2), by_room.round(2), by_t.round(2),
        by_lead_time.round(2), r
    )


def enrich_conversion_profiles(conversion_room, conversion_treatment, room, treatment, cfg):
    room_cols = [
        "room_id", "confirmed_bookings", "revenue", "avg_adr", "avg_booking_window",
        "cancellation_rate_pct", "operating_occupancy_pct", "operating_revpar", "reliability"
    ]
    room_profile = conversion_room.merge(room[room_cols], on="room_id", how="left")
    room_profile["conversion_reliability"] = room_profile.quoted_requests.apply(
        lambda n: reliability_label(n, cfg)
    )
    room_profile["conversion_vs_quoted_room_avg_pp"] = (
        room_profile.same_room_conversion_pct
        - np.average(
            room_profile.same_room_conversion_pct.fillna(0),
            weights=room_profile.quoted_requests.clip(lower=1),
        )
    )
    room_profile = room_profile.sort_values(
        ["same_room_conversion_pct", "quoted_requests"], ascending=[False, False]
    )

    treatment_cols = [
        "arrangement_code", "comparability_group", "confirmed_bookings", "revenue",
        "avg_adr", "avg_booking_window", "cancellation_rate_pct", "revenue_per_booking",
        "reliability"
    ]
    treatment_profile = conversion_treatment.merge(
        treatment[treatment_cols], on="arrangement_code", how="left"
    )
    treatment_profile["conversion_reliability"] = treatment_profile.quoted_requests.apply(
        lambda n: reliability_label(n, cfg)
    )
    comparable = treatment_profile.comparability_group.eq("COMPARABLE_COMMERCIAL")
    if comparable.any():
        benchmark = np.average(
            treatment_profile.loc[comparable, "same_treatment_conversion_pct"].fillna(0),
            weights=treatment_profile.loc[comparable, "quoted_requests"].clip(lower=1),
        )
    else:
        benchmark = np.average(
            treatment_profile.same_treatment_conversion_pct.fillna(0),
            weights=treatment_profile.quoted_requests.clip(lower=1),
        )
    treatment_profile["conversion_vs_comparable_avg_pp"] = (
        treatment_profile.same_treatment_conversion_pct - benchmark
    )
    treatment_profile = treatment_profile.sort_values(
        ["same_treatment_conversion_pct", "quoted_requests"], ascending=[False, False]
    )
    return room_profile.round(2), treatment_profile.round(2)


def booking_pace(bookings, as_of, cfg):
    b = confirmed_bookings(bookings, cfg)
    b = b[b.checkout_date.le(as_of) & b.lead_time_days.ge(0)].copy()
    b["arrival_month"] = b.checkin_date.dt.to_period("M").astype(str)
    rows = []
    for m, g in b.groupby("arrival_month"):
        row = {"arrival_month": m, "final_confirmed_bookings": g.booking_code.nunique()}
        for t in cfg.pace_thresholds:
            row[f"booked_by_{t}d_pct"] = g.lead_time_days.ge(t).mean() * 100
        rows.append(row)
    return pd.DataFrame(rows).sort_values("arrival_month").round(2)


def _relative_table(df, entity_col, metrics):
    out = df[[entity_col] + metrics].copy()
    for metric in metrics:
        avg = df[metric].mean()
        out[f"{metric}_vs_population_pct"] = np.where(avg == 0, np.nan, (df[metric] / avg - 1) * 100)
    return out.round(2)


def _rankings(df, entity_col, metrics, min_volume_col=None, min_volume=0, group_col=None, group_value=None):
    x = df.copy()
    if group_col is not None:
        x = x[x[group_col].eq(group_value)]
    if min_volume_col:
        x = x[x[min_volume_col].ge(min_volume)]
    rows = []
    lower_is_better = {"cancellation_rate_pct"}
    for metric in metrics:
        ranked = x.dropna(subset=[metric]).sort_values(metric, ascending=metric in lower_is_better).reset_index(drop=True)
        for i, r in ranked.iterrows():
            row = {"metric": metric, "rank": i + 1, entity_col: r[entity_col], "value": r[metric]}
            if "confirmed_bookings" in r.index:
                row["observations"] = r["confirmed_bookings"]
            if "reliability" in r.index:
                row["reliability"] = r["reliability"]
            rows.append(row)
    return pd.DataFrame(rows).round(2)


def _pairwise_matrix(df, entity_col, metric, min_volume_col=None, min_volume=0, difference_mode="relative_pct"):
    x = df.copy()
    if min_volume_col:
        x = x[x[min_volume_col].ge(min_volume)]
    x = x[[entity_col, metric]].dropna().drop_duplicates(entity_col)
    entities = x[entity_col].tolist()
    values = dict(zip(x[entity_col], x[metric]))
    rows = []
    for base in entities:
        row = {entity_col: base}
        for other in entities:
            if base == other:
                row[other] = np.nan
            elif difference_mode == "percentage_points":
                row[other] = values[other] - values[base]
            else:
                denom = values[base]
                row[other] = np.nan if denom == 0 else (values[other] / denom - 1) * 100
        rows.append(row)
    return pd.DataFrame(rows).round(2)


def room_booking_window_distribution(bookings, as_of, cfg):
    b = confirmed_bookings(bookings, cfg)
    b = b[b.checkout_date.le(as_of) & b.lead_time_days.ge(0)].copy()
    b["booking_window_band"] = pd.cut(b.lead_time_days, bins=cfg.booking_window_bins, labels=cfg.booking_window_labels)
    counts = b.groupby(["room_name", "booking_window_band"], observed=True).booking_code.nunique().rename("bookings").reset_index()
    counts["share_pct"] = counts.bookings / counts.groupby("room_name").bookings.transform("sum") * 100
    return counts.pivot(index="booking_window_band", columns="room_name", values="share_pct").fillna(0).reset_index().round(2)


def treatment_booking_window_distribution(bookings, as_of, cfg):
    b = confirmed_bookings(bookings, cfg)
    b = b[b.checkout_date.le(as_of) & b.lead_time_days.ge(0)].copy()
    b["booking_window_band"] = pd.cut(b.lead_time_days, bins=cfg.booking_window_bins, labels=cfg.booking_window_labels)
    counts = b.groupby(["arrangement_name", "booking_window_band"], observed=True).booking_code.nunique().rename("bookings").reset_index()
    counts["share_pct"] = counts.bookings / counts.groupby("arrangement_name").bookings.transform("sum") * 100
    return counts.pivot(index="booking_window_band", columns="arrangement_name", values="share_pct").fillna(0).reset_index().round(2)


def _relative_to_benchmarks(df, entity_col, metrics, benchmarks):
    out = df[[entity_col] + metrics].copy()
    for metric in metrics:
        benchmark = benchmarks.get(metric, df[metric].mean())
        out[f"{metric}_benchmark"] = benchmark
        out[f"{metric}_vs_benchmark_pct"] = np.where(benchmark == 0, np.nan, (df[metric] / benchmark - 1) * 100)
    return out.round(2)


def build_comparison_profiles(room, treatment, cfg: AnalysisConfig):
    room = room.copy()
    treatment = treatment.copy()

    property_adr = room.revenue.sum() / room.room_nights.sum()
    property_los = room.room_nights.sum() / room.confirmed_bookings.sum()
    property_bw = np.average(room.avg_booking_window, weights=room.confirmed_bookings)
    property_canc = room.canceled_bookings.sum() / room.total_bookings.sum() * 100
    property_oper_occ = (
        room.operating_occupied_room_nights.sum() / room.operating_available_room_nights.sum() * 100
        if "operating_available_room_nights" in room and room.operating_available_room_nights.sum() else np.nan
    )
    property_oper_revpar = property_adr * property_oper_occ / 100 if pd.notna(property_oper_occ) else np.nan

    room_commercial = room[[
        "room_name", "confirmed_bookings", "revenue", "revenue_share_pct", "avg_adr",
        "operating_revpar", "reliability"
    ]].copy()
    room_commercial["bookings_vs_peer_median_pct"] = (room.confirmed_bookings / room.confirmed_bookings.median() - 1) * 100
    room_commercial["revenue_vs_peer_median_pct"] = (room.revenue / room.revenue.median() - 1) * 100
    room_commercial["adr_vs_property_pct"] = (room.avg_adr / property_adr - 1) * 100
    room_commercial["revpar_vs_property_pct"] = (room.operating_revpar / property_oper_revpar - 1) * 100

    room_demand = room[[
        "room_name", "confirmed_bookings", "avg_los", "avg_booking_window",
        "operating_occupancy_pct", "reliability"
    ]].copy()
    room_demand["los_vs_property_pct"] = (room.avg_los / property_los - 1) * 100
    room_demand["booking_window_vs_property_pct"] = (room.avg_booking_window / property_bw - 1) * 100
    room_demand["occupancy_vs_property_pp"] = room.operating_occupancy_pct - property_oper_occ

    room_risk = room[[
        "room_name", "total_bookings", "canceled_bookings", "cancellation_rate_pct", "reliability"
    ]].copy()
    room_risk["cancellation_vs_property_pp"] = room.cancellation_rate_pct - property_canc

    comparable = treatment[treatment.comparability_group.eq("COMPARABLE_COMMERCIAL")].copy()
    if comparable.empty:
        comparable = treatment.copy()
    t_adr = comparable.revenue.sum() / comparable.room_nights.sum()
    t_los = comparable.room_nights.sum() / comparable.confirmed_bookings.sum()
    t_bw = np.average(comparable.avg_booking_window, weights=comparable.confirmed_bookings)
    t_canc = comparable.canceled_bookings.sum() / comparable.total_bookings.sum() * 100
    t_rpb = comparable.revenue.sum() / comparable.confirmed_bookings.sum()
    treatment_comparison = treatment[[
        "arrangement_name", "comparability_group", "confirmed_bookings", "revenue", "revenue_share_pct",
        "avg_adr", "avg_los", "avg_booking_window", "cancellation_rate_pct",
        "revenue_per_booking", "reliability"
    ]].copy()
    treatment_comparison["adr_vs_comparable_property_pct"] = (treatment.avg_adr / t_adr - 1) * 100
    treatment_comparison["los_vs_comparable_property_pct"] = (treatment.avg_los / t_los - 1) * 100
    treatment_comparison["booking_window_vs_comparable_property_pct"] = (treatment.avg_booking_window / t_bw - 1) * 100
    treatment_comparison["cancellation_vs_comparable_property_pp"] = treatment.cancellation_rate_pct - t_canc
    treatment_comparison["revenue_per_booking_vs_comparable_property_pct"] = (treatment.revenue_per_booking / t_rpb - 1) * 100

    room_rank_metrics = ["avg_adr", "revenue", "avg_booking_window", "cancellation_rate_pct", "operating_occupancy_pct", "operating_revpar", "avg_los"]
    treatment_rank_metrics = ["avg_adr", "revenue", "avg_booking_window", "cancellation_rate_pct", "avg_los", "revenue_per_booking"]
    profiles = {
        "room_commercial_comparison": room_commercial.round(2),
        "room_demand_comparison": room_demand.round(2),
        "room_risk_comparison": room_risk.round(2),
        "room_rankings": _rankings(room, "room_name", room_rank_metrics, "confirmed_bookings", cfg.reliability_medium_min),
        "treatment_comparison": treatment_comparison.round(2),
        "treatment_rankings": _rankings(
            treatment, "arrangement_name", treatment_rank_metrics, "confirmed_bookings",
            cfg.reliability_medium_min, "comparability_group", "COMPARABLE_COMMERCIAL"
        ),
    }
    relative_metrics = ["avg_adr", "avg_booking_window", "operating_revpar"]
    pp_metrics = ["cancellation_rate_pct", "operating_occupancy_pct"]
    for metric in relative_metrics:
        profiles[f"room_pairwise_{metric}"] = _pairwise_matrix(
            room, "room_name", metric, "confirmed_bookings", cfg.reliability_medium_min, "relative_pct"
        )
    for metric in pp_metrics:
        profiles[f"room_pairwise_{metric}"] = _pairwise_matrix(
            room, "room_name", metric, "confirmed_bookings", cfg.reliability_medium_min, "percentage_points"
        )
    return profiles


# ---------------------------------------------------------------------------
# Cross-dimensional discovery (Layer 3)
# ---------------------------------------------------------------------------
def _add_time_dimensions(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    x = df.copy()
    d = pd.to_datetime(x[date_col], errors="coerce")
    x["stay_year"] = d.dt.year.astype("Int64")
    x["stay_month_num"] = d.dt.month.astype("Int64")
    x["stay_month"] = d.dt.to_period("M").astype(str)
    x["stay_week"] = d.dt.isocalendar().week.astype("Int64")
    x["season_band"] = np.select(
        [d.dt.month.isin([7, 8]), d.dt.month.isin([6, 9])],
        ["PEAK", "SHOULDER"],
        default="LOW",
    )
    return x


def _booking_window_band_series(df: pd.DataFrame, cfg: AnalysisConfig) -> pd.Series:
    return pd.cut(
        df.lead_time_days,
        bins=cfg.booking_window_bins,
        labels=cfg.booking_window_labels,
    )


def _period_is_complete(month_series: pd.Series, as_of: pd.Timestamp) -> pd.Series:
    periods = pd.PeriodIndex(month_series.astype(str), freq="M")
    month_end = periods.to_timestamp(how="end").normalize()
    return month_end <= pd.Timestamp(as_of).normalize()


def room_time_crossovers(bookings, occ_daily, as_of, cfg):
    """Room × year × month/season, plus booking-window slices."""
    b = bookings[bookings.checkout_date.le(as_of)].copy()
    b = _add_time_dimensions(b, "checkin_date")
    c = confirmed_bookings(b, cfg)
    c = c[c.lead_time_days.ge(0)].copy()
    c["booking_window_band"] = _booking_window_band_series(c, cfg)

    group = ["stay_year", "stay_month", "season_band", "room_id", "room_name"]
    total = b.groupby(group).booking_code.nunique().rename("total_bookings")
    canc = canceled_bookings(b, cfg).groupby(group).booking_code.nunique().rename("canceled_bookings")
    base = c.groupby(group, observed=True).agg(
        confirmed_bookings=("booking_code", "nunique"),
        room_nights=("nights", "sum"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
    ).join(total).join(canc).reset_index()
    base["canceled_bookings"] = base.canceled_bookings.fillna(0)
    base["cancellation_rate_pct"] = np.where(
        base.total_bookings.gt(0), base.canceled_bookings / base.total_bookings * 100, np.nan
    )

    occ = _add_time_dimensions(occ_daily.copy(), "stay_date")
    occm = occ.groupby(group).agg(
        occupied_room_nights=("occupied_rooms", "sum"),
        available_room_nights=("capacity", "sum"),
    ).reset_index()
    occm["occupancy_pct"] = np.where(
        occm.available_room_nights.gt(0),
        occm.occupied_room_nights / occm.available_room_nights * 100,
        np.nan,
    )
    base = base.merge(occm, on=group, how="left")
    base["revpar"] = base.avg_adr * base.occupancy_pct / 100
    base["reliability"] = base.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))

    window_group = group + ["booking_window_band"]
    window = c.groupby(window_group, observed=True).agg(
        confirmed_bookings=("booking_code", "nunique"),
        room_nights=("nights", "sum"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
    ).reset_index()
    window["reliability"] = window.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))
    return base.round(2), window.round(2)


def treatment_time_crossovers(bookings, as_of, cfg):
    """Treatment × year × month/season, plus booking-window slices."""
    b = bookings[bookings.checkout_date.le(as_of)].copy()
    b = _add_time_dimensions(b, "checkin_date")
    c = confirmed_bookings(b, cfg)
    c = c[c.lead_time_days.ge(0)].copy()
    c["booking_window_band"] = _booking_window_band_series(c, cfg)

    group = ["stay_year", "stay_month", "season_band", "arrangement_code", "arrangement_name"]
    total = b.groupby(group, dropna=False).booking_code.nunique().rename("total_bookings")
    canc = canceled_bookings(b, cfg).groupby(group, dropna=False).booking_code.nunique().rename("canceled_bookings")
    base = c.groupby(group, dropna=False).agg(
        confirmed_bookings=("booking_code", "nunique"),
        room_nights=("nights", "sum"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
        revenue_per_booking=("total_stay_amount", "mean"),
    ).join(total).join(canc).reset_index()
    base["canceled_bookings"] = base.canceled_bookings.fillna(0)
    base["cancellation_rate_pct"] = np.where(
        base.total_bookings.gt(0), base.canceled_bookings / base.total_bookings * 100, np.nan
    )
    base["comparability_group"] = base.arrangement_code.apply(lambda v: classify_treatment(v, cfg))
    base["reliability"] = base.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))

    window = c.groupby(group + ["booking_window_band"], dropna=False, observed=True).agg(
        confirmed_bookings=("booking_code", "nunique"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
    ).reset_index()
    window["comparability_group"] = window.arrangement_code.apply(lambda v: classify_treatment(v, cfg))
    window["reliability"] = window.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))
    return base.round(2), window.round(2)


def room_treatment_crossovers(bookings, as_of, cfg):
    """Room × treatment × year × month/season."""
    b = confirmed_bookings(bookings, cfg)
    b = b[b.checkout_date.le(as_of) & b.lead_time_days.ge(0)].copy()
    b = _add_time_dimensions(b, "checkin_date")
    out = b.groupby([
        "stay_year", "stay_month", "season_band", "room_id", "room_name",
        "arrangement_code", "arrangement_name"
    ], dropna=False).agg(
        confirmed_bookings=("booking_code", "nunique"),
        revenue=("total_stay_amount", "sum"),
        avg_adr=("adr", "mean"),
        avg_los=("nights", "mean"),
        avg_booking_window=("lead_time_days", "mean"),
    ).reset_index()
    out["comparability_group"] = out.arrangement_code.apply(lambda v: classify_treatment(v, cfg))
    out["reliability"] = out.confirmed_bookings.apply(lambda n: reliability_label(n, cfg))
    return out.round(2)


def conversion_crossovers(requests, quotes, bookings, as_of, cfg):
    """Conversion × year × month/season × booking window × quoted room/treatment.

    Only completed stay months are used in the historical crossover layer, so partial
    future 2026 periods are not compared as if they were final.
    """
    r = match_requests_to_bookings(requests, bookings, cfg)
    r = _add_time_dimensions(r, "checkin_date")
    r = r[r.lead_time_days.ge(0)].copy()
    r["booking_window_band"] = _booking_window_band_series(r, cfg)
    r["period_complete"] = _period_is_complete(r.stay_month, as_of)
    r_hist = r[r.period_complete].copy()

    base_group = ["stay_year", "stay_month", "season_band", "booking_window_band"]
    base = r_hist.groupby(base_group, observed=True).agg(
        requests=("request_code", "nunique"),
        quoted_requests=("request_code", lambda s: s[r_hist.loc[s.index, "has_quotation"].eq(1)].nunique()),
        converted_requests=("converted", "sum"),
        quote_rate_pct=("has_quotation", "mean"),
        conversion_pct=("converted", "mean"),
        avg_requested_lead_time=("lead_time_days", "mean"),
    ).reset_index()
    base[["quote_rate_pct", "conversion_pct"]] *= 100

    q = quotes.merge(
        r_hist[[
            "request_code", "stay_year", "stay_month", "season_band", "booking_window_band",
            "converted", "booked_room_id", "booked_arrangement_code"
        ]],
        on="request_code", how="inner"
    )
    qr = q.groupby([
        "request_code", "stay_year", "stay_month", "season_band", "booking_window_band",
        "room_id", "room_name"
    ], observed=True, as_index=False).agg(
        converted=("converted", "max"),
        booked_room_id=("booked_room_id", "first"),
        avg_quote_amount=("total_amount", "mean"),
    )
    qr["same_room_conversion"] = (qr.converted.eq(1) & qr.room_id.eq(qr.booked_room_id)).astype(int)
    by_room = qr.groupby([
        "stay_year", "stay_month", "season_band", "booking_window_band", "room_id", "room_name"
    ], observed=True).agg(
        quoted_requests=("request_code", "nunique"),
        overall_converted_requests=("converted", "sum"),
        same_room_converted_requests=("same_room_conversion", "sum"),
        avg_quote_amount=("avg_quote_amount", "mean"),
    ).reset_index()
    by_room["overall_conversion_pct"] = by_room.overall_converted_requests / by_room.quoted_requests * 100
    by_room["same_room_conversion_pct"] = by_room.same_room_converted_requests / by_room.quoted_requests * 100

    qt = q.groupby([
        "request_code", "stay_year", "stay_month", "season_band", "booking_window_band",
        "arrangement_code", "arrangement_name"
    ], dropna=False, observed=True, as_index=False).agg(
        converted=("converted", "max"),
        booked_arrangement_code=("booked_arrangement_code", "first"),
        avg_quote_amount=("total_amount", "mean"),
    )
    qt["same_treatment_conversion"] = (
        qt.converted.eq(1) & qt.arrangement_code.eq(qt.booked_arrangement_code)
    ).astype(int)
    by_treatment = qt.groupby([
        "stay_year", "stay_month", "season_band", "booking_window_band",
        "arrangement_code", "arrangement_name"
    ], dropna=False, observed=True).agg(
        quoted_requests=("request_code", "nunique"),
        overall_converted_requests=("converted", "sum"),
        same_treatment_converted_requests=("same_treatment_conversion", "sum"),
        avg_quote_amount=("avg_quote_amount", "mean"),
    ).reset_index()
    by_treatment["overall_conversion_pct"] = by_treatment.overall_converted_requests / by_treatment.quoted_requests * 100
    by_treatment["same_treatment_conversion_pct"] = (
        by_treatment.same_treatment_converted_requests / by_treatment.quoted_requests * 100
    )
    by_treatment["comparability_group"] = by_treatment.arrangement_code.apply(lambda v: classify_treatment(v, cfg))
    return base.round(2), by_room.round(2), by_treatment.round(2)
