from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AnalysisConfig:
    confirmed_statuses: Tuple[str, ...] = ("CONFIRMED",)
    canceled_statuses: Tuple[str, ...] = ("CANCELED",)
    pending_statuses: Tuple[str, ...] = ("CONFIRM_WAITING",)
    pseudo_room_tokens: Tuple[str, ...] = ("OVER", "JOLLY")
    booking_window_bins: Tuple[int, ...] = (-1, 7, 14, 30, 60, 90, 180, 10000)
    booking_window_labels: Tuple[str, ...] = ("0-7", "8-14", "15-30", "31-60", "61-90", "91-180", "181+")
    pace_thresholds: Tuple[int, ...] = (7, 14, 30, 60, 90, 180)
    conversion_match_max_days: int = 365

    # Reliability policy used consistently in tables, rankings, and patterns.
    reliability_medium_min: int = 30
    reliability_high_min: int = 100
    reliability_low_min: int = 10

    # An inferred operating month must have meaningful occupied inventory.
    # This does not claim to be the hotel's official opening calendar.
    operating_month_min_occupied_room_nights: int = 30
    operating_month_min_calendar_occupancy_pct: float = 2.0

    # Treatments whose revenue semantics appear comparable to normal board/rate plans.
    comparable_treatment_codes: Tuple[str, ...] = ("HB", "FB", "BB", "OB", "HBL")
    special_treatment_codes: Tuple[str, ...] = ("MUL", "RS", "SP", "NB")
