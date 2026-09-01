from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
ACTIONS = OUTPUT / "actionable_recommendations.csv"

def _groups(frame, keys):
    return {
        key: np.sort(g["creation_datetime"].dt.normalize().values.astype("datetime64[D]"))
        for key, g in frame.groupby(keys)
    }

def _count(groups, key, dt):
    arr = groups.get(key, np.array([], dtype="datetime64[D]"))
    return int(np.searchsorted(arr, np.datetime64(pd.Timestamp(dt).date(), "D"), side="right"))

def _baseline(groups, year, month, dims, lead):
    vals = []
    for py in range(2024, year):
        dt = pd.Timestamp(py, month, 1) - pd.Timedelta(days=lead)
        vals.append(_count(groups, (py, month, *dims), dt))
    return float(np.mean(vals)) if vals else np.nan

def _trigger(groups, year, month, dims, direction):
    if year <= 2024:
        return None
    start = pd.Timestamp(year, month, 1)
    for lead in range(180, 13, -1):
        dt = start - pd.Timedelta(days=lead)
        cur = _count(groups, (year, month, *dims), dt)
        base = _baseline(groups, year, month, dims, lead)
        if not np.isfinite(base) or base < 10 or cur < 20:
            continue
        ratio = cur / base
        threshold = 1.25 if direction == "UP" else 0.80
        if (direction == "UP" and ratio < threshold) or (direction == "DOWN" and ratio > threshold):
            continue
        lead2 = max(lead - 7, 13)
        dt2 = start - pd.Timedelta(days=lead2)
        cur2 = _count(groups, (year, month, *dims), dt2)
        base2 = _baseline(groups, year, month, dims, lead2)
        if not np.isfinite(base2) or base2 < 10:
            continue
        ratio2 = cur2 / base2
        sustained = ratio2 >= 1.20 if direction == "UP" else ratio2 <= 0.85
        if sustained:
            return dt.date().isoformat(), lead, cur, round(base,1), round(ratio,2)
    return None

def main():
    requests = pd.read_csv(
        DATA / "fact_richieste.csv",
        usecols=["request_code","creation_datetime","checkin_date"],
        parse_dates=["creation_datetime","checkin_date"]
    )
    quotes = pd.read_csv(
        DATA / "fact_richieste_preventivi.csv",
        usecols=["request_code","room_name","arrangement_name"]
    )
    actions = pd.read_csv(ACTIONS)

    rq = quotes.merge(requests, on="request_code", how="left").dropna(
        subset=["creation_datetime","checkin_date","room_name"]
    )
    rq["stay_year"] = rq["checkin_date"].dt.year
    rq["stay_month_num"] = rq["checkin_date"].dt.month

    room_events = rq.drop_duplicates(["request_code","room_name"])
    pkg_events = rq.dropna(subset=["arrangement_name"]).drop_duplicates(
        ["request_code","room_name","arrangement_name"]
    )
    room_groups = _groups(room_events, ["stay_year","stay_month_num","room_name"])
    pkg_groups = _groups(pkg_events, ["stay_year","stay_month_num","room_name","arrangement_name"])

    rows = []
    relevant = actions[actions["action_type"].isin(["PRICE_UP","PRICE_DOWN","PACKAGE_PRICE_UP"])]
    for _, a in relevant.iterrows():
        y, m, room = int(a["stay_year"]), int(a["stay_month_num"]), a["room_name"]
        typ = a["action_type"]
        if typ == "PACKAGE_PRICE_UP":
            treatment = a["treatment"]
            t = _trigger(pkg_groups, y, m, (room, treatment), "UP")
        else:
            treatment = np.nan
            t = _trigger(room_groups, y, m, (room,), "UP" if typ == "PRICE_UP" else "DOWN")
        row = {
            "stay_year": y, "stay_month_num": m, "room_name": room,
            "treatment": treatment, "action_type": typ,
            "recommended_action": a["action"],
            "economic_value_eur": a["economic_value_eur"],
            "confidence": a["confidence"],
        }
        if t:
            row.update(dict(
                decision_date=t[0], lead_days_to_stay_month=t[1],
                requests_to_date=t[2], historical_requests_same_lead=t[3],
                request_pace_index=t[4], timing_status="HISTORICAL_TRIGGER_FOUND",
                timing_reason=f"Request pace reached {t[4]:.2f}× prior-year(s) pace at the same lead time and remained beyond the trigger for at least 7 days."
            ))
        else:
            row.update(dict(
                decision_date=np.nan, lead_days_to_stay_month=np.nan,
                requests_to_date=np.nan, historical_requests_same_lead=np.nan,
                request_pace_index=np.nan, timing_status="NO_ROBUST_REQUEST_PACE_TRIGGER",
                timing_reason="Retrospective price action exists, but request pace alone did not meet the robust timing trigger."
            ))
        rows.append(row)

    OUTPUT.mkdir(exist_ok=True)
    out = pd.DataFrame(rows).sort_values(
        ["stay_year","stay_month_num","action_type","economic_value_eur"],
        ascending=[True,True,True,False]
    )
    out.to_csv(OUTPUT / "timed_pricing_decisions.csv", index=False)
    print(f"Wrote {len(out)} timed pricing decisions to output/timed_pricing_decisions.csv")

if __name__ == "__main__":
    main()
