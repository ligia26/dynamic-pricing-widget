from pathlib import Path
import pandas as pd
from .validation import validate_inputs

DATE_COLS={"fact_prenotazioni":["checkin_date","checkout_date","creation_datetime","cancellation_datetime"],"fact_richieste":["checkin_date","checkout_date","creation_datetime"],"fact_richieste_preventivi":["creation_datetime"],"fact_prenotazioni_ricavi_giorno":["stay_date"]}
FILES=["fact_prenotazioni","fact_prenotazioni_ospiti","fact_prenotazioni_ricavi_giorno","fact_richieste","fact_richieste_preventivi","dim_camere","dim_trattamenti"]

def load_all(data_dir: Path) -> dict[str,pd.DataFrame]:
    result={}
    for name in FILES:
        path=data_dir/f"{name}.csv"
        if not path.exists(): raise FileNotFoundError(f"Missing required dataset: {path}")
        df=pd.read_csv(path,low_memory=False)
        for col in DATE_COLS.get(name,[]):
            if col in df.columns: df[col]=pd.to_datetime(df[col],errors="coerce")
        result[name]=df
    validation=validate_inputs(result)
    if validation.errors: raise ValueError("Input validation failed: "+"; ".join(validation.errors))
    return result

def infer_as_of(data: dict[str,pd.DataFrame]) -> pd.Timestamp:
    candidates=[]
    for name,col in [("fact_prenotazioni","creation_datetime"),("fact_richieste","creation_datetime"),("fact_richieste_preventivi","creation_datetime")]:
        s=data[name][col].dropna()
        if not s.empty: candidates.append(s.max())
    if not candidates: raise ValueError("Cannot infer analysis as-of date")
    return min(max(candidates),pd.Timestamp.now()).normalize()
