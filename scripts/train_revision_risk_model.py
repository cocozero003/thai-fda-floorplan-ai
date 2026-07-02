"""Train the Phase 4 synthetic revision-risk model."""

from __future__ import annotations

import argparse
import json

from floorplan_ai.models.train_revision_risk import train_revision_risk_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train synthetic advisory revision-risk model.")
    parser.add_argument("--training-data", required=True, help="Path to synthetic training CSV.")
    parser.add_argument("--model-output", required=True, help="Path to write model pickle.")
    parser.add_argument("--metrics-output", required=True, help="Path to write synthetic metrics JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = train_revision_risk_model(args.training_data, args.model_output)
    with open(args.metrics_output, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
    print("Synthetic revision-risk model written to " + args.model_output)
    print("Synthetic metrics written to " + args.metrics_output)
    print(metrics["warning"])


if __name__ == "__main__":
    main()
