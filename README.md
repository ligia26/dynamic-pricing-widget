# Dynamic Pricing Pattern & Analytics MVP — La Casarana

A deterministic, auditable first analytical layer for the seven Booking Designer exports.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The downloaded `output/` folder is empty. Running the code validates the inputs, infers the extraction as-of date, clears previous generated files, and creates a fresh `output/pattern_report.md` plus supporting CSV tables.

## Architecture

- `loaders.py`: typed date loading and as-of inference
- `validation.py`: schema and integrity checks
- `config.py`: explicit analytical policy
- `analytics.py`: booking window, completed-stay KPIs, capacity-aware occupancy, one-to-one conversion proxy, booking pace
- `patterns.py`: deterministic patterns with minimum evidence thresholds
- `report.py`: human-readable report
- `pipeline.py`: orchestration only
- `tests/`: core regression tests

## Important analytical choices

- Confirmed, cancelled, and waiting statuses are separated.
- Completed historical stays are separated from future on-books demand.
- Occupancy includes zero-occupancy dates and uses sellable physical capacity only.
- OVER/JOLLY/deleted/zero-capacity room types are excluded from capacity.
- Request conversion uses a documented one-to-one proxy because no direct request-to-booking key exists.
- Quote-room and quote-treatment tables avoid counting multiple solutions as multiple conversions.
- Reliable current pickup and movement detection will require recurring dataset snapshots.
