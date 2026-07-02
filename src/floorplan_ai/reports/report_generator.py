"""Generate officer-facing synthetic workflow reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def generate_json_report(session_result: dict[str, Any], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(session_result, indent=2), encoding="utf-8")
    return output


def generate_markdown_report(session_result: dict[str, Any], output_path: str | Path) -> Path:
    case = session_result["case"]
    report = session_result["screening_report"]
    prediction = session_result.get("ml_prediction")
    lines = [
        "# Synthetic Thai FDA Floor-Plan Pre-Screening Report",
        "",
        "This report is advisory decision support only. It does not approve or reject any application.",
        "Human Thai FDA officers remain responsible for all regulatory decisions.",
        "Phase 2 is deferred. This repository currently uses synthetic data only.",
        "Real Thai FDA de-identified data and expert annotation are required before validation or operational use.",
        "",
        "## Case",
        "",
        f"- Case ID: {case['case_id']}",
        f"- Annotation ID: {case['annotation']['annotation_id']}",
        f"- Status: {case['status']}",
        f"- Officer comment: {case.get('officer_comment') or 'None recorded'}",
        f"- Officer override: {case.get('officer_override') or 'None recorded'}",
        "",
        "## Rule-Based Findings",
        "",
        f"- Finding count: {report['summary']['finding_count']}",
    ]
    for finding in report.get("findings", []):
        lines.extend(
            [
                "",
                f"### {finding['rule_id']}: {finding['name']}",
                "",
                f"- Severity: {finding['severity']}",
                f"- Confidence: {finding['confidence']}",
                f"- Explanation: {finding['explanation']}",
                f"- Recommended officer review action: {finding['recommended_action']}",
            ]
        )

    lines.extend(["", "## Synthetic ML Revision-Risk Prediction", ""])
    if prediction is None:
        lines.append("No synthetic ML prediction was included in this workflow run.")
    else:
        lines.append(f"- Advisory revision-risk class: {prediction['revision_risk_class']}")
        for label, probability in prediction["class_probabilities"].items():
            lines.append(f"- Probability {label}: {probability:.3f}")
        lines.append("- Warning: " + prediction["warning"])

    lines.extend(["", "## Audit Log", ""])
    for entry in session_result["audit_log"]["entries"]:
        lines.append(f"- {entry['timestamp']} | {entry['actor']} | {entry['action']}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
