
from __future__ import annotations
from pathlib import Path
import pandas as pd
from .validation import validate_input_files, validate_loaded
from .constants import NON_SELLABLE_ROOM_TOKENS
from .utils import booking_window, season

def load_data(input_dir: Path):
    validate_input_files(input_dir)
    b=pd.read_csv(input_dir/"fact_prenotazioni.csv")
    r=pd.read_csv(input_dir/"fact_richieste.csv")
    q=pd.read_csv(input_dir/"fact_richieste_preventivi.csv")
    rooms=pd.read_csv(input_dir/"dim_camere.csv")
    treatments=pd.read_csv(input_dir/"dim_trattamenti.csv")
    daily=pd.read_csv(input_dir/"fact_prenotazioni_ricavi_giorno.csv")

    for df, cols in [
        (b,["checkin_date","checkout_date","creation_datetime","cancellation_datetime"]),
        (r,["checkin_date","checkout_date","creation_datetime"]),
        (q,["creation_datetime"]),
        (daily,["stay_date"])
    ]:
        for c in cols:
            if c in df:
                df[c]=pd.to_datetime(df[c],errors="coerce")

    validate_loaded(b,r,q,rooms)
    return b,r,q,rooms,treatments,daily

def sellable_rooms(rooms):
    x=rooms.copy()
    x["quantity"]=pd.to_numeric(x["quantity"],errors="coerce").fillna(0)
    mask=(x["deleted"].fillna(0).eq(0)) & (x["quantity"]>0)
    for token in NON_SELLABLE_ROOM_TOKENS:
        mask &= ~x["name"].str.contains(token,case=False,na=False)
    return x[mask].copy()

def enrich_bookings(b):
    x=b.copy()
    x["stay_year"]=x["checkin_date"].dt.year
    x["stay_month_num"]=x["checkin_date"].dt.month
    x["season"]=x["stay_month_num"].map(season)
    x["booking_window"]=x["lead_time_days"].map(booking_window)
    x["room_nights"]=pd.to_numeric(x["nights"],errors="coerce").fillna(0)
    x["adr"]=pd.to_numeric(x["adr"],errors="coerce")
    x["total_stay_amount"]=pd.to_numeric(x["total_stay_amount"],errors="coerce").fillna(0)
    return x

def enrich_requests(r):
    x=r.copy()
    x["stay_year"]=x["checkin_date"].dt.year
    x["stay_month_num"]=x["checkin_date"].dt.month
    x["season"]=x["stay_month_num"].map(season)
    x["booking_window"]=x["lead_time_days"].map(booking_window)
    return x
