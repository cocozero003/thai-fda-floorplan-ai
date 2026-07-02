"""Run advisory floor-plan pre-screening from the command line."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.features.spatial_features import extract_spatial_features
from floorplan_ai.heatmap.generator import generate_heatmap
from floorplan_ai.rules.rule_engine import ADVISORY_NOTICE, evaluate_rules, generate_risk_report, load_rules


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run advisory Thai FDA floor-plan screening prototype.")
    parser.add_argument("--annotation", required=True, help="Path to synthetic annotation JSON.")
    parser.add_argument("--rules", required=True, help="Path to GMP-oriented rule YAML.")
    parser.add_argument("--output", required=True, help="Path to write advisory JSON report.")
    parser.add_argument("--heatmap", required=True, help="Path to write advisory heatmap PNG.")
    parser.add_argument("--image", default=None, help="Optional floor-plan image path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(ADVISORY_NOTICE)
    annotation_path = Path(args.annotation)
    rules_path = Path(args.rules)
    output_path = Path(args.output)
    heatmap_path = Path(args.heatmap)

    annotation = FloorPlanAnnotation.model_validate_json(annotation_path.read_text(encoding="utf-8"))
    features = extract_spatial_features(annotation)
    rules = load_rules(rules_path)
    findings = evaluate_rules(annotation, rules, features)
    report = generate_risk_report(annotation, findings, features)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    generate_heatmap(annotation, findings, image_path=args.image, output_path=heatmap_path)

    print(f"Advisory report written to {output_path}")
    print(f"Advisory heatmap written to {heatmap_path}")
    print(f"Findings requiring officer review: {len(findings)}")


if __name__ == "__main__":
    main()
