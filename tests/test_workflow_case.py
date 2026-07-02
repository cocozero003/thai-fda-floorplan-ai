from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.workflow.case import ScreeningCase
from floorplan_ai.workflow.review_session import ReviewSession


def test_screening_case_and_review_session_are_advisory() -> None:
    annotation = FloorPlanAnnotation.model_validate_json(
        Path("data/sample_synthetic/annotation_simple_factory.json").read_text(encoding="utf-8")
    )
    case = ScreeningCase.from_annotation(annotation, case_id="synthetic-test-case")
    session = ReviewSession(case, "configs/rules_gmp_thai_fda.yaml")
    session.add_officer_input("Needs officer review.", "No automatic decision.")

    result = session.run()

    assert result["advisory_only"] is True
    assert result["human_review_required"] is True
    assert result["case"]["officer_comment"] == "Needs officer review."
    assert result["screening_report"]["summary"]["finding_count"] >= 1
    assert result["audit_log"]["entries"]
