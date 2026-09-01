
from __future__ import annotations
import numpy as np
import pandas as pd
from .data import enrich_requests

def build_conversion(bookings, requests, quotes):
    """
    Directional demand-quality proxy.

    There is no direct request->booking foreign key in the source data.
    We match customer + requested check-in and then evaluate whether the
    booked room equals a quoted room. This metric is explicitly not treated
    as audited CRM conversion.
    """
    req=enrich_requests(requests)
    quoted=quotes[["request_code","room_name","arrangement_name"]].drop_duplicates().rename(
        columns={"room_name":"room_name_quoted","arrangement_name":"arrangement_name_quoted"}
    )
    qr=req.merge(quoted,on="request_code",how="inner",validate="one_to_many")

    confirmed=bookings[bookings["status"].eq("CONFIRMED")][
        ["customer_code","checkin_date","room_name","arrangement_name"]
    ].drop_duplicates().rename(
        columns={"room_name":"room_name_booked","arrangement_name":"arrangement_name_booked"}
    )

    matched=qr.merge(confirmed,on=["customer_code","checkin_date"],how="left")
    matched["converted_any"]=matched["room_name_booked"].notna().astype(int)
    matched["converted_same_room"]=matched["room_name_booked"].eq(matched["room_name_quoted"]).astype(int)

    keys=["stay_year","stay_month_num","season","booking_window","room_name_quoted"]
    g=(matched.groupby(keys,dropna=False).agg(
        quoted_requests=("request_code","nunique"),
        converted_requests=("converted_any","sum"),
        same_room_converted=("converted_same_room","sum")
    ).reset_index().rename(columns={"room_name_quoted":"room_name"}))
    g["conversion_pct"]=np.where(g["quoted_requests"]>0,100*g["same_room_converted"]/g["quoted_requests"],np.nan)
    return g
