"""Synthetic dataset generation for advisory revision-risk modeling."""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Any


FEATURE_NAMES = [
    "finding_count",
    "high_severity_count",
    "review_severity_count",
    "room_count",
    "object_count",
    "flow_intersection_count",
    "has_toilet_near_production",
    "has_waste_flow_intersection",
    "unknown_room_count",
    "handwashing_point_count",
]

CLASS_NAMES = ["low", "medium", "high"]

SYNTHETIC_DATA_WARNING = (
    "Synthetic-data prototype only. No real Thai FDA records were used, and no real-world "
    "validation or operational performance is claimed."
)


def _risk_class(row: dict[str, float]) -> str:
    score = (
        row["finding_count"]
        + 2 * row["high_severity_count"]
        + row["flow_intersection_count"]
        + 2 * row["has_toilet_near_production"]
        + 2 * row["has_waste_flow_intersection"]
        + row["unknown_room_count"]
        - 0.5 * row["handwashing_point_count"]
    )
    if score >= 7:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def generate_synthetic_training_rows(count: int = 120, seed: int = 42) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    rows: list[dict[str, Any]] = []
    for index in range(count):
        high_severity_count = rng.randint(0, 3)
        review_severity_count = rng.randint(0, 4)
        flow_intersection_count = rng.randint(0, 3)
        has_toilet_near_production = rng.randint(0, 1)
        has_waste_flow_intersection = rng.randint(0, 1)
        unknown_room_count = rng.randint(0, 2)
        handwashing_point_count = rng.randint(0, 3)
        finding_count = high_severity_count + review_severity_count + flow_intersection_count
        row: dict[str, Any] = {
            "case_id": f"synthetic-training-{index + 1:04d}",
            "finding_count": finding_count,
            "high_severity_count": high_severity_count,
            "review_severity_count": review_severity_count,
            "room_count": rng.randint(5, 14),
            "object_count": rng.randint(4, 20),
            "flow_intersection_count": flow_intersection_count,
            "has_toilet_near_production": has_toilet_near_production,
            "has_waste_flow_intersection": has_waste_flow_intersection,
            "unknown_room_count": unknown_room_count,
            "handwashing_point_count": handwashing_point_count,
        }
        row["revision_risk_class"] = _risk_class(row)
        rows.append(row)
    return rows


def write_synthetic_training_csv(rows: list[dict[str, Any]], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["case_id", *FEATURE_NAMES, "revision_risk_class"]
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output


def load_training_csv(path: str | Path) -> tuple[list[list[float]], list[str], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    features = [[float(row[name]) for name in FEATURE_NAMES] for row in rows]
    labels = [str(row["revision_risk_class"]) for row in rows]
    return features, labels, rows


def features_from_screening_report(report: dict[str, Any]) -> dict[str, float]:
    findings = report.get("findings", [])
    severity_counts = report.get("summary", {}).get("severity_counts", {})
    features = report.get("features", {})
    object_counts = features.get("object_count_by_class", {})
    flow_intersections = features.get("flow_intersections", [])
    related_rules = {finding.get("rule_id", "") for finding in findings}
    return {
        "finding_count": float(len(findings)),
        "high_severity_count": float(severity_counts.get("high", 0)),
        "review_severity_count": float(severity_counts.get("review", 0)),
        "room_count": float(sum(1 for key in object_counts if key.endswith("_area") or key in {"toilet", "corridor", "unknown"})),
        "object_count": float(sum(count for key, count in object_counts.items() if not key.endswith("_area") and key not in {"toilet", "corridor", "unknown"})),
        "flow_intersection_count": float(len(flow_intersections)),
        "has_toilet_near_production": float(any("toilet" in rule_id for rule_id in related_rules)),
        "has_waste_flow_intersection": float(any("waste" in rule_id for rule_id in related_rules)),
        "unknown_room_count": float(object_counts.get("unknown", 0) + object_counts.get("unlabeled_room", 0)),
        "handwashing_point_count": float(object_counts.get("handwashing_point", 0)),
    }


def feature_vector(feature_map: dict[str, float]) -> list[float]:
    return [float(feature_map.get(name, 0.0)) for name in FEATURE_NAMES]
