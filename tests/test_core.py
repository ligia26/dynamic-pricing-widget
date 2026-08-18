import pandas as pd
from src.dynamic_pricing_patterns.config import AnalysisConfig
from src.dynamic_pricing_patterns.analytics import sellable_rooms, occupancy_monthly


def test_pseudo_rooms_excluded():
    rooms = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Standard", "* OVER *", "Old"],
        "quantity": [10, 10, 0],
        "deleted": [0, 0, 1],
    })
    assert sellable_rooms(rooms, AnalysisConfig()).id.tolist() == [1]


def test_monthly_occupancy_is_weighted():
    d = pd.to_datetime(["2026-01-01", "2026-01-01"])
    occ = pd.DataFrame({
        "stay_date": d,
        "occupied_rooms": [5, 1],
        "capacity": [10, 2],
        "occupancy_pct": [50, 50],
        "over_capacity_flag": [False, False],
    })
    result = occupancy_monthly(occ).iloc[0]
    assert result.property_occupancy_pct == 50.0
