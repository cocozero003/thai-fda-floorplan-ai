from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.features.spatial_features import extract_spatial_features
from floorplan_ai.rules.rule_engine import ADVISORY_NOTICE, evaluate_rules, generate_risk_report, load_rules


SAMPLE = Path("data/sample_synthetic/annotation_simple_factory.json")
RULES = Path("configs/rules_gmp_thai_fda.yaml")


def test_rule_engine_generates_advisory_findings() -> None:
    annotation = FloorPlanAnnotation.model_validate_json(SAMPLE.read_text(encoding="utf-8"))
    features = extract_spatial_features(annotation)
    findings = evaluate_rules(annotation, load_rules(RULES), features)

    rule_ids = {finding.rule_id for finding in findings}
    assert "GMP-001" in rule_ids
    assert "GMP-002" in rule_ids
    assert "GMP-003" in rule_ids
    assert all(finding.advisory_only for finding in findings)
    assert all(finding.requires_officer_review for finding in findings)


def test_report_preserves_human_review_language() -> None:
    annotation = FloorPlanAnnotation.model_validate_json(SAMPLE.read_text(encoding="utf-8"))
    features = extract_spatial_features(annotation)
    findings = evaluate_rules(annotation, load_rules(RULES), features)
    report = generate_risk_report(annotation, findings, features)

    assert report["advisory_only"] is True
    assert report["human_review_required"] is True
    assert "does not approve or reject" in report["advisory_notice"]
    assert ADVISORY_NOTICE == report["advisory_notice"]
