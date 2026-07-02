from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.reports.report_generator import generate_json_report, generate_markdown_report
from floorplan_ai.workflow.case import ScreeningCase
from floorplan_ai.workflow.review_session import ReviewSession


def test_report_generator_writes_markdown_and_json(tmp_path: Path) -> None:
    annotation = FloorPlanAnnotation.model_validate_json(
        Path("data/sample_synthetic/annotation_simple_factory.json").read_text(encoding="utf-8")
    )
    session = ReviewSession(ScreeningCase.from_annotation(annotation), "configs/rules_gmp_thai_fda.yaml")
    result = session.run()

    markdown_path = generate_markdown_report(result, tmp_path / "report.md")
    json_path = generate_json_report(result, tmp_path / "report.json")

    assert markdown_path.exists()
    assert json_path.exists()
    assert "Phase 2 is deferred" in markdown_path.read_text(encoding="utf-8")
    assert "advisory_only" in json_path.read_text(encoding="utf-8")
