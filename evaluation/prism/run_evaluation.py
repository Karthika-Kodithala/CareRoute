# Person 3: replace with the actual PRISM/evaluation execution.
# Keep the V1 and V2 scenario set identical for a defensible comparison.

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "datasets" / "scenarios.json"

if __name__ == "__main__":
    scenarios = json.loads(DATASET.read_text(encoding="utf-8"))
    print(f"Loaded {len(scenarios)} scenarios.")
    print("TODO: execute evaluation and save results under results/v1 or results/v2.")
