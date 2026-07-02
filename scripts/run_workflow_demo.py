"""Run the Phase 5 synthetic officer workflow demo."""

from __future__ import annotations

import argparse
from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.reports.report_generator import generate_json_report, generate_markdown_report
from floorplan_ai.workflow.case import ScreeningCase
from floorplan_ai.workflow.review_session import ReviewSession


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run synthetic officer workflow simulation.")
    parser.add_argument("--annotation", required=True, help="Path to synthetic annotation JSON.")
    parser.add_argument("--rules", required=True, help="Path to rule YAML.")
    parser.add_argument("--markdown-output", required=True, help="Path to write officer Markdown report.")
    parser.add_argument("--json-output", required=True, help="Path to write officer JSON report.")
    parser.add_argument("--audit-output", required=True, help="Path to write audit log JSON.")
    parser.add_argument("--model", default=None, help="Optional trained synthetic model pickle.")
    parser.add_argument("--officer-comment", default="Synthetic officer comment for demo review.")
    parser.add_argument("--officer-override", default="No automatic decision. Officer review remains required.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    annotation = FloorPlanAnnotation.model_validate_json(Path(args.annotation).read_text(encoding="utf-8"))
    case = ScreeningCase.from_annotation(annotation, case_id="synthetic-workflow-case-001")
    session = ReviewSession(case, args.rules, args.model)
    session.add_officer_input(args.officer_comment, args.officer_override)
    result = session.run()
    markdown_path = generate_markdown_report(result, args.markdown_output)
    json_path = generate_json_report(result, args.json_output)
    audit_path = session.audit_log.write_json(args.audit_output)
    print("Phase 5 synthetic officer workflow demo complete.")
    print("Officer Markdown report written to " + str(markdown_path))
    print("Officer JSON report written to " + str(json_path))
    print("Audit log written to " + str(audit_path))
    print("Advisory only. Human Thai FDA officers remain responsible for decisions.")


if __name__ == "__main__":
    main()
