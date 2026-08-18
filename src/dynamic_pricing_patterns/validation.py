from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

REQUIRED_COLUMNS = {
    "fact_prenotazioni": {"booking_code","status","checkin_date","checkout_date","creation_datetime","customer_code","room_id","room_name","arrangement_code","arrangement_name","total_stay_amount","adr","lead_time_days","is_canceled"},
    "fact_richieste": {"request_code","checkin_date","checkout_date","creation_datetime","customer_code","has_quotation","lead_time_days"},
    "fact_richieste_preventivi": {"request_code","quotation_code","creation_datetime","room_id","arrangement_code","total_amount"},
    "dim_camere": {"id","name","quantity","deleted"},
    "dim_trattamenti": {"code","name"},
}

@dataclass
class ValidationResult:
    checks: pd.DataFrame
    errors: list[str]

def validate_inputs(data: dict[str, pd.DataFrame]) -> ValidationResult:
    rows=[]; errors=[]
    for name, required in REQUIRED_COLUMNS.items():
        if name not in data:
            errors.append(f"Missing dataset: {name}")
            continue
        missing=sorted(required-set(data[name].columns))
        rows.append({"check":"required_columns","dataset":name,"status":"PASS" if not missing else "FAIL","details":", ".join(missing)})
        if missing: errors.append(f"{name}: missing columns {missing}")
    if errors: return ValidationResult(pd.DataFrame(rows), errors)
    b=data["fact_prenotazioni"]
    duplicate=int(b["booking_code"].duplicated().sum())
    rows.append({"check":"unique_booking_code","dataset":"fact_prenotazioni","status":"PASS" if duplicate==0 else "WARN","details":str(duplicate)})
    invalid_stays=int((b["checkout_date"]<=b["checkin_date"]).fillna(False).sum())
    rows.append({"check":"checkout_after_checkin","dataset":"fact_prenotazioni","status":"PASS" if invalid_stays==0 else "FAIL","details":str(invalid_stays)})
    if invalid_stays: errors.append(f"fact_prenotazioni: {invalid_stays} invalid stay ranges")
    negative_amounts=int((b["total_stay_amount"]<0).fillna(False).sum())
    rows.append({"check":"nonnegative_stay_amount","dataset":"fact_prenotazioni","status":"PASS" if negative_amounts==0 else "WARN","details":str(negative_amounts)})
    q=data["fact_richieste_preventivi"]
    orphan=int((~q["request_code"].isin(data["fact_richieste"]["request_code"])).sum())
    rows.append({"check":"quotes_have_request","dataset":"fact_richieste_preventivi","status":"PASS" if orphan==0 else "WARN","details":str(orphan)})
    return ValidationResult(pd.DataFrame(rows), errors)
