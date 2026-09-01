from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from dynamic_pricing_patterns.pipeline import run

if __name__ == "__main__":
    summary = run(ROOT / "data", ROOT / "output", ROOT / "config.json")
    print("\nDynamic Pricing Engine v0.6")
    print("=" * 40)
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("\nOutputs written to ./output")
