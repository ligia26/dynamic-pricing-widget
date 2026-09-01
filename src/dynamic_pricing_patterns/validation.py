
from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED = {
    "fact_prenotazioni.csv": {
        "booking_code","status","checkin_date","checkout_date","nights","customer_code",
        "room_id","room_name","arrangement_code","arrangement_name","total_stay_amount",
        "adr","creation_datetime","lead_time_days","is_canceled"
    },
    "fact_richieste.csv": {
        "request_code","checkin_date","checkout_date","customer_code","creation_datetime",
        "lead_time_days","has_quotation"
    },
    "fact_richieste_preventivi.csv": {
        "request_code","customer_code","room_id","room_name","arrangement_code",
        "arrangement_name","creation_datetime","total_amount"
    },
    "dim_camere.csv": {"id","name","quantity","deleted"},
    "dim_trattamenti.csv": {"code","name"},
    "fact_prenotazioni_ricavi_giorno.csv": {
        "booking_code","stay_date","stay_amount","status","room_id","in_stay_range"
    },
}

class DataContractError(ValueError):
    pass

def validate_input_files(input_dir: Path):
    errors=[]
    stats=[]
    for filename, required in REQUIRED.items():
        path=input_dir/filename
        if not path.exists():
            errors.append(f"Missing required file: {filename}")
            continue
        df=pd.read_csv(path, nrows=5)
        missing=sorted(required-set(df.columns))
        if missing:
            errors.append(f"{filename}: missing columns {missing}")
        stats.append({"file":filename,"columns":len(df.columns)})
    if errors:
        raise DataContractError("; ".join(errors))
    return pd.DataFrame(stats)

def validate_loaded(bookings, requests, quotes, rooms):
    checks=[]
    checks.append(("duplicate_booking_code", int(bookings["booking_code"].duplicated().sum()), 0))
    checks.append(("negative_booking_nights", int((pd.to_numeric(bookings["nights"],errors="coerce")<0).sum()), 0))
    checks.append(("missing_booking_checkin", int(bookings["checkin_date"].isna().sum()), 0))
    checks.append(("missing_booking_room", int(bookings["room_id"].isna().sum()), 0))
    # Negative stay amounts can be legitimate adjustments/refunds in source exports.
    # They are reported as a warning rather than silently removed or treated as corruption.
    negative_amounts=int((pd.to_numeric(bookings["total_stay_amount"],errors="coerce")<0).sum())
    checks.append(("duplicate_request_code", int(requests["request_code"].duplicated().sum()), 0))
    checks.append(("orphan_quote_request", int((~quotes["request_code"].isin(requests["request_code"])).sum()), 0))
    checks.append(("duplicate_room_id", int(rooms["id"].duplicated().sum()), 0))
    out=pd.DataFrame(checks,columns=["check","value","expected_max"])
    out["passed"]=out["value"]<=out["expected_max"]
    out=pd.concat([out,pd.DataFrame([{
        "check":"negative_stay_amount_warning","value":negative_amounts,
        "expected_max":negative_amounts,"passed":True
    }])],ignore_index=True)
    critical=out[~out["passed"]]
    if not critical.empty:
        raise DataContractError("Critical data quality failure: " + critical.to_dict(orient="records").__repr__())
    return out
