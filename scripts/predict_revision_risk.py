"""Predict advisory revision risk from a synthetic screening report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from floorplan_ai.models.dataset import features_from_screening_report
from floorplan_ai.models.predict_revision_risk import predict_revision_risk


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict synthetic advisory revision risk.")
    parser.add_argument("--model", required=True, help="Path to trained synthetic model pickle.")
    parser.add_argument("--screening-report", required=True, help="Path to advisory screening report JSON.")
    parser.add_argument("--output", required=True, help="Path to write prediction JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = json.loads(Path(args.screening_report).read_text(encoding="utf-8"))
    prediction = predict_revision_risk(args.model, features_from_screening_report(report))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(prediction, indent=2), encoding="utf-8")
    print("Advisory synthetic revision-risk prediction written to " + str(output))
    print(prediction["warning"])


if __name__ == "__main__":
    main()
