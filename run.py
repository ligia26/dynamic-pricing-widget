from pathlib import Path
from src.dynamic_pricing_patterns.pipeline import run_pipeline

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    run_pipeline(root / "data", root / "output")
    print(f"Done. Open: {root / 'output' / 'pattern_report.md'}")
