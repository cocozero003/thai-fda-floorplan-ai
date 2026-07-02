"""Streamlit demonstration app for advisory floor-plan pre-screening."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.features.spatial_features import extract_spatial_features
from floorplan_ai.heatmap.generator import generate_heatmap
from floorplan_ai.rules.rule_engine import ADVISORY_NOTICE, evaluate_rules, generate_risk_report, load_rules


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ANNOTATION = REPO_ROOT / "data" / "sample_synthetic" / "annotation_simple_factory.json"
DEFAULT_RULES = REPO_ROOT / "configs" / "rules_gmp_thai_fda.yaml"


def _load_annotation(path: Path) -> FloorPlanAnnotation:
    return FloorPlanAnnotation.model_validate_json(path.read_text(encoding="utf-8"))


def main() -> None:
    st.set_page_config(page_title="Thai FDA Floor-Plan Pre-Screening Prototype", layout="wide")
    st.title("Thai FDA Food Manufacturing Floor-Plan Pre-Screening")
    st.warning(ADVISORY_NOTICE)
    st.caption("Synthetic Phase 1 research prototype. Do not use real applicant or confidential business data.")

    uploaded_image = st.file_uploader("Optional floor-plan image", type=["png", "jpg", "jpeg"])

    annotation = _load_annotation(DEFAULT_ANNOTATION)
    features = extract_spatial_features(annotation)
    rules = load_rules(DEFAULT_RULES)
    findings = evaluate_rules(annotation, rules, features)
    report = generate_risk_report(annotation, findings, features)

    with tempfile.TemporaryDirectory() as tmp_dir:
        image_path = None
        if uploaded_image is not None:
            image_path = Path(tmp_dir) / uploaded_image.name
            image_path.write_bytes(uploaded_image.getvalue())

        heatmap_path = Path(tmp_dir) / "streamlit_heatmap.png"
        generate_heatmap(annotation, findings, image_path=image_path, output_path=heatmap_path)

        left, right = st.columns([1, 1])
        with left:
            st.subheader("Risk Findings")
            finding_rows = [
                {
                    "rule_id": finding.rule_id,
                    "name": finding.name,
                    "severity": finding.severity,
                    "confidence": finding.confidence,
                    "requires_officer_review": finding.requires_officer_review,
                    "advisory_only": finding.advisory_only,
                    "explanation": finding.explanation,
                    "recommended_action": finding.recommended_action,
                }
                for finding in findings
            ]
            st.dataframe(pd.DataFrame(finding_rows), use_container_width=True, hide_index=True)

        with right:
            st.subheader("Advisory Heatmap")
            st.image(str(heatmap_path), use_container_width=True)

    st.subheader("Export")
    st.download_button(
        "Download advisory JSON report",
        data=json.dumps(report, indent=2),
        file_name="advisory_floorplan_report.json",
        mime="application/json",
    )

    st.subheader("Feature Summary")
    st.json(
        {
            "object_count_by_class": features["object_count_by_class"],
            "room_area_by_type": features["room_area_by_type"],
            "flow_intersections": features["flow_intersections"],
        }
    )


if __name__ == "__main__":
    main()
