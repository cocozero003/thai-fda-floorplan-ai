"""Explainable advisory rule engine for synthetic floor-plan annotations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.features.spatial_features import extract_spatial_features, minimum_distance_between_classes


ADVISORY_NOTICE = (
    "This report is advisory decision support only. It does not approve or reject any application. "
    "Human Thai FDA officers remain responsible for regulatory decisions."
)


class RiskFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    name: str
    severity: str
    explanation: str
    recommended_action: str
    related_object_ids: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    requires_officer_review: bool = True
    advisory_only: bool = True


def load_rules(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as file:
        payload = yaml.safe_load(file)
    rules = payload.get("rules", []) if isinstance(payload, dict) else []
    for rule in rules:
        rule["advisory_only"] = True
    return rules


def _distance_key(class_a: str, class_b: str) -> str:
    return f"{class_a}__{class_b}"


def _get_distance(
    annotation: FloorPlanAnnotation,
    features: dict[str, Any],
    class_a: str,
    class_b: str,
) -> dict[str, Any] | None:
    distances = features.get("minimum_distances", {})
    return distances.get(_distance_key(class_a, class_b)) or minimum_distance_between_classes(
        annotation, class_a, class_b
    )


def _make_finding(
    rule: dict[str, Any],
    explanation: str,
    related_object_ids: list[str],
    confidence: float,
) -> RiskFinding:
    severity = str(rule.get("severity", "review"))
    return RiskFinding(
        rule_id=str(rule["rule_id"]),
        name=str(rule["name"]),
        severity=severity,
        explanation=explanation,
        recommended_action=str(rule["recommended_action"]),
        related_object_ids=sorted(set(related_object_ids)),
        confidence=confidence,
        requires_officer_review=True,
        advisory_only=True,
    )


def _evaluate_minimum_distance(
    annotation: FloorPlanAnnotation,
    features: dict[str, Any],
    rule: dict[str, Any],
) -> RiskFinding | None:
    condition = rule["condition"]
    threshold = float(condition["threshold"])
    distance_record = _get_distance(annotation, features, condition["class_a"], condition["class_b"])
    if distance_record is None:
        return None

    distance = float(distance_record["distance"])
    operator = condition.get("operator", "less_than")
    triggered = distance < threshold if operator == "less_than" else distance <= threshold
    if not triggered:
        return None

    explanation = rule["explanation_template"].format(distance=distance, threshold=threshold)
    return _make_finding(
        rule,
        explanation,
        [distance_record["object_id_a"], distance_record["object_id_b"]],
        confidence=0.85,
    )


def _evaluate_flow_intersection(features: dict[str, Any], rule: dict[str, Any]) -> RiskFinding | None:
    condition = rule["condition"]
    target_types = {condition["flow_type_a"], condition["flow_type_b"]}
    related_ids: list[str] = []

    for intersection in features.get("flow_intersections", []):
        intersection_types = {intersection["flow_type_a"], intersection["flow_type_b"]}
        if target_types == intersection_types:
            related_ids.extend([intersection["flow_id_a"], intersection["flow_id_b"]])
            related_ids.extend(intersection.get("related_object_ids", []))

    if not related_ids:
        return None

    return _make_finding(rule, rule["explanation_template"], related_ids, confidence=0.9)


def _evaluate_sanitation_before_entry(
    annotation: FloorPlanAnnotation,
    features: dict[str, Any],
    rule: dict[str, Any],
) -> RiskFinding | None:
    condition = rule["condition"]
    threshold = float(condition["max_distance_to_door"])
    handwash_count = features.get("object_count_by_class", {}).get(condition["handwashing_class"], 0)
    production_doors = [
        obj
        for obj in annotation.objects
        if obj.object_type == "door"
        and any(room.room_id == obj.room_id and room.room_type == condition["production_class"] for room in annotation.rooms)
    ]

    if not production_doors:
        return None

    if handwash_count == 0:
        explanation = rule["explanation_template"].format(threshold=threshold)
        return _make_finding(rule, explanation, [obj.object_id for obj in production_doors], confidence=0.75)

    distance_record = _get_distance(annotation, features, "door", condition["handwashing_class"])
    if distance_record is None or float(distance_record["distance"]) > threshold:
        explanation = rule["explanation_template"].format(threshold=threshold)
        related_ids = [obj.object_id for obj in production_doors]
        if distance_record is not None:
            related_ids.append(distance_record["object_id_b"])
        return _make_finding(rule, explanation, related_ids, confidence=0.7)

    return None


def _evaluate_adjacent_object(
    annotation: FloorPlanAnnotation,
    features: dict[str, Any],
    rule: dict[str, Any],
) -> RiskFinding | None:
    condition = rule["condition"]
    threshold = float(condition["threshold"])
    distance_record = _get_distance(annotation, features, condition["class_a"], condition["class_b"])
    if distance_record is None:
        return None

    distance = float(distance_record["distance"])
    if distance > threshold:
        return None

    explanation = rule["explanation_template"].format(distance=distance, threshold=threshold)
    return _make_finding(
        rule,
        explanation,
        [distance_record["object_id_a"], distance_record["object_id_b"]],
        confidence=0.65,
    )


def _evaluate_waste_area_near_clean_zone(
    annotation: FloorPlanAnnotation,
    features: dict[str, Any],
    rule: dict[str, Any],
) -> RiskFinding | None:
    condition = rule["condition"]
    threshold = float(condition["threshold"])
    best: dict[str, Any] | None = None
    for clean_class in condition["clean_zone_classes"]:
        distance_record = _get_distance(annotation, features, condition["waste_class"], clean_class)
        if distance_record is not None and (best is None or distance_record["distance"] < best["distance"]):
            best = distance_record

    if best is None or float(best["distance"]) >= threshold:
        return None

    explanation = rule["explanation_template"].format(distance=float(best["distance"]), threshold=threshold)
    return _make_finding(rule, explanation, [best["object_id_a"], best["object_id_b"]], confidence=0.85)


def _evaluate_unknown_room_near_production(
    annotation: FloorPlanAnnotation,
    features: dict[str, Any],
    rule: dict[str, Any],
) -> RiskFinding | None:
    condition = rule["condition"]
    threshold = float(condition["threshold"])
    best: dict[str, Any] | None = None
    for unknown_class in condition["unknown_classes"]:
        distance_record = _get_distance(annotation, features, unknown_class, condition["production_class"])
        if distance_record is not None and (best is None or distance_record["distance"] < best["distance"]):
            best = distance_record

    if best is None or float(best["distance"]) >= threshold:
        return None

    explanation = rule["explanation_template"].format(distance=float(best["distance"]), threshold=threshold)
    return _make_finding(rule, explanation, [best["object_id_a"], best["object_id_b"]], confidence=0.55)


def evaluate_rules(
    annotation: FloorPlanAnnotation,
    rules: list[dict[str, Any]],
    features: dict[str, Any] | None = None,
) -> list[RiskFinding]:
    features = features or extract_spatial_features(annotation)
    findings: list[RiskFinding] = []

    evaluators = {
        "minimum_distance": _evaluate_minimum_distance,
        "flow_intersection": lambda _annotation, rule_features, rule: _evaluate_flow_intersection(rule_features, rule),
        "sanitation_before_entry": _evaluate_sanitation_before_entry,
        "adjacent_object": _evaluate_adjacent_object,
        "waste_area_near_clean_zone": _evaluate_waste_area_near_clean_zone,
        "unknown_room_near_production": _evaluate_unknown_room_near_production,
    }

    for rule in rules:
        condition_type = rule.get("condition", {}).get("type")
        evaluator = evaluators.get(condition_type)
        if evaluator is None:
            continue
        finding = evaluator(annotation, features, rule)
        if finding is not None:
            findings.append(finding)

    return findings


def generate_risk_report(
    annotation: FloorPlanAnnotation,
    findings: list[RiskFinding],
    features: dict[str, Any] | None = None,
) -> dict[str, Any]:
    severity_counts: dict[str, int] = {}
    for finding in findings:
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

    return {
        "annotation_id": annotation.annotation_id,
        "advisory_only": True,
        "advisory_notice": ADVISORY_NOTICE,
        "human_review_required": True,
        "summary": {
            "finding_count": len(findings),
            "severity_counts": severity_counts,
        },
        "findings": [finding.model_dump() for finding in findings],
        "features": features or extract_spatial_features(annotation),
    }
