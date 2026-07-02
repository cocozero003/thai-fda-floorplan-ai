"""Streamlit demonstration app for advisory floor-plan pre-screening."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.cv.annotation_converter import detections_to_annotation
from floorplan_ai.cv.detector import detect_synthetic_floorplan
from floorplan_ai.cv.preprocess import preprocess_image
from floorplan_ai.features.spatial_features import extract_spatial_features
from floorplan_ai.heatmap.generator import generate_heatmap
from floorplan_ai.models.dataset import (
    SYNTHETIC_DATA_WARNING,
    features_from_screening_report,
    generate_synthetic_training_rows,
    write_synthetic_training_csv,
)
from floorplan_ai.models.predict_revision_risk import predict_revision_risk
from floorplan_ai.models.train_revision_risk import train_revision_risk_model
from floorplan_ai.reports.report_generator import generate_json_report, generate_markdown_report
from floorplan_ai.rules.rule_engine import ADVISORY_NOTICE, evaluate_rules, generate_risk_report, load_rules
from floorplan_ai.workflow.case import ScreeningCase
from floorplan_ai.workflow.review_session import ReviewSession
from scripts.generate_synthetic_floorplan_image import generate_synthetic_floorplan_image


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ANNOTATION = REPO_ROOT / "data" / "sample_synthetic" / "annotation_simple_factory.json"
DEFAULT_RULES = REPO_ROOT / "configs" / "rules_gmp_thai_fda.yaml"


def _load_annotation(path: Path) -> FloorPlanAnnotation:
    return FloorPlanAnnotation.model_validate_json(path.read_text(encoding="utf-8"))


def main() -> None:
    st.set_page_config(page_title="Thai FDA Floor-Plan Pre-Screening Prototype", layout="wide")
    st.title("Thai FDA Food Manufacturing Floor-Plan Pre-Screening")
    st.warning(ADVISORY_NOTICE)
    st.caption(
        "Phase 2 is deferred. This app uses synthetic data only and makes no real-world validation claim."
    )

    annotation = _load_annotation(DEFAULT_ANNOTATION)
    features = extract_spatial_features(annotation)
    rules = load_rules(DEFAULT_RULES)
    findings = evaluate_rules(annotation, rules, features)
    report = generate_risk_report(annotation, findings, features)

    tab_phase_1, tab_phase_3, tab_phase_4, tab_phase_5 = st.tabs(
        [
            "Phase 1 Rule-Based Screening",
            "Phase 3 Synthetic CV",
            "Phase 4 Synthetic ML",
            "Phase 5 Officer Workflow",
        ]
    )

    with tab_phase_1:
        uploaded_image = st.file_uploader("Optional synthetic floor-plan image", type=["png", "jpg", "jpeg"])
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

        st.subheader("Feature Summary")
        st.json(
            {
                "object_count_by_class": features["object_count_by_class"],
                "room_area_by_type": features["room_area_by_type"],
                "flow_intersections": features["flow_intersections"],
            }
        )

    with tab_phase_3:
        with tempfile.TemporaryDirectory() as tmp_dir:
            synthetic_image_path = Path(tmp_dir) / "synthetic_floorplan.png"
            generate_synthetic_floorplan_image(annotation, synthetic_image_path)
            preprocessed = preprocess_image(synthetic_image_path)
            detections = detect_synthetic_floorplan(synthetic_image_path)
            detected_annotation = detections_to_annotation(
                detections,
                preprocessed["width"],
                preprocessed["height"],
                annotation_id="streamlit-synthetic-cv-detected",
            )
            st.subheader("Generated Synthetic Floor Plan")
            st.image(str(synthetic_image_path), use_container_width=True)
            st.subheader("Synthetic Detections")
            st.dataframe(pd.DataFrame([d.__dict__ for d in detections]), use_container_width=True, hide_index=True)
            st.download_button(
                "Download detected synthetic annotation JSON",
                data=json.dumps(detected_annotation.model_dump(), indent=2),
                file_name="synthetic_cv_detected_annotation.json",
                mime="application/json",
            )
        st.info("Phase 3 is a synthetic color-based prototype. It is not trained on real Thai FDA data.")

    with tab_phase_4:
        with tempfile.TemporaryDirectory() as tmp_dir:
            training_csv = Path(tmp_dir) / "synthetic_training.csv"
            model_path = Path(tmp_dir) / "synthetic_revision_risk_model.pkl"
            write_synthetic_training_csv(generate_synthetic_training_rows(160, seed=42), training_csv)
            metrics = train_revision_risk_model(training_csv, model_path)
            prediction = predict_revision_risk(model_path, features_from_screening_report(report))
            st.subheader("Advisory Revision-Risk Prediction")
            st.json(prediction)
            st.subheader("Synthetic Holdout Metrics")
            st.json(metrics)
        st.warning(SYNTHETIC_DATA_WARNING)

    with tab_phase_5:
        officer_comment = st.text_area("Officer comment", value="")
        officer_override = st.text_input("Officer override or disposition note", value="")
        case = ScreeningCase.from_annotation(annotation, case_id="streamlit-synthetic-case-001")
        session = ReviewSession(case, DEFAULT_RULES)
        session.add_officer_input(officer_comment, officer_override)
        workflow_result = session.run()

        with tempfile.TemporaryDirectory() as tmp_dir:
            markdown_path = Path(tmp_dir) / "officer_report.md"
            json_path = Path(tmp_dir) / "officer_report.json"
            generate_markdown_report(workflow_result, markdown_path)
            generate_json_report(workflow_result, json_path)
            markdown_report = markdown_path.read_text(encoding="utf-8")
            json_report = json_path.read_text(encoding="utf-8")

        st.subheader("Officer Report Preview")
        st.markdown(markdown_report)
        st.download_button(
            "Download officer Markdown report",
            data=markdown_report,
            file_name="synthetic_officer_report.md",
            mime="text/markdown",
        )
        st.download_button(
            "Download officer JSON report",
            data=json_report,
            file_name="synthetic_officer_report.json",
            mime="application/json",
        )
        st.subheader("Audit Log")
        st.json(workflow_result["audit_log"])

    st.subheader("Export Phase 1 JSON")
    st.download_button(
        "Download advisory JSON report",
        data=json.dumps(report, indent=2),
        file_name="advisory_floorplan_report.json",
        mime="application/json",
    )


if __name__ == "__main__":
    main()
