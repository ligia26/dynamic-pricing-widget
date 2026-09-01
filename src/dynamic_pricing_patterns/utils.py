
from __future__ import annotations
import pandas as pd

def booking_window(days):
    if pd.isna(days):
        return "UNKNOWN"
    d = float(days)
    if d <= 7: return "0-7"
    if d <= 14: return "8-14"
    if d <= 30: return "15-30"
    if d <= 60: return "31-60"
    if d <= 90: return "61-90"
    if d <= 180: return "91-180"
    return "181+"

def season(month):
    # MVP property-specific mapping. Kept in one place and configurable later.
    return {5:"SHOULDER", 6:"SHOULDER", 7:"PEAK", 8:"PEAK", 9:"SHOULDER"}.get(int(month), "OTHER")

def safe_div(num, den):
    return num / den.where(den != 0)

def confidence_from_score(score: int) -> str:
    return "HIGH" if score >= 4 else ("MEDIUM" if score >= 3 else "LOW")
