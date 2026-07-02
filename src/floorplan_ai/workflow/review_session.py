"""Run synthetic officer review sessions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from floorplan_ai.features.spatial_features import extract_spatial_features
from floorplan_ai.models.dataset import features_from_screening_report
from floorplan_ai.models.predict_revision_risk import predict_revision_risk
from floorplan_ai.rules.rule_engine import ADVISORY_NOTICE, evaluate_rules, generate_risk_report, load_rules
from floorplan_ai.workflow.audit_log import AuditLog
from floorplan_ai.workflow.case import ScreeningCase


class ReviewSession:
    def __init__(self, case: ScreeningCase, rules_path: str | Path, model_path: str | Path | None = None) -> None:
        self.case = case
        self.rules_path = Path(rules_path)
        self.model_path = Path(model_path) if model_path is not None else None
        self.audit_log = AuditLog()
        self.audit_log.record("session_created", details={"case_id": case.case_id})

    def run(self) -> dict[str, Any]:
        self.audit_log.record("rule_screening_started", details={"rules_path": str(self.rules_path)})
        features = extract_spatial_features(self.case.annotation)
        rules = load_rules(self.rules_path)
        findings = evaluate_rules(self.case.annotation, rules, features)
        screening_report = generate_risk_report(self.case.annotation, findings, features)
        self.audit_log.record("rule_screening_completed", details={"finding_count": len(findings)})

        ml_prediction = None
        if self.model_path is not None:
            self.audit_log.record("synthetic_ml_prediction_started", details={"model_path": str(self.model_path)})
            ml_prediction = predict_revision_risk(self.model_path, features_from_screening_report(screening_report))
            self.audit_log.record(
                "synthetic_ml_prediction_completed",
                details={"revision_risk_class": ml_prediction["revision_risk_class"]},
            )

        return {
            "case": self.case.model_dump(),
            "screening_report": screening_report,
            "ml_prediction": ml_prediction,
            "audit_log": self.audit_log.to_dict(),
            "advisory_notice": ADVISORY_NOTICE,
            "advisory_only": True,
            "human_review_required": True,
            "synthetic_data_only": True,
            "warning": (
                "Phase 2 is deferred. This workflow uses synthetic data only and does not claim "
                "real-world validation."
            ),
        }

    def add_officer_input(self, comment: str, override: str) -> None:
        self.case = self.case.with_officer_input(comment, override)
        self.audit_log.record(
            "officer_input_recorded",
            actor="synthetic_officer",
            details={"has_comment": bool(comment), "has_override": bool(override)},
        )
