# Explainable Regulatory Health Informatics for Thai FDA Food Manufacturing Floor-Plan Pre-Screening

This repository contains a synthetic research prototype for GMP-oriented food manufacturing floor-plan pre-screening. It is designed as an advisory decision-support tool that helps Thai FDA officers review synthetic floor-plan annotations for spatial layout risks such as unsafe adjacency, crossing flows, insufficient sanitation access, toilet proximity to production areas, waste flow crossing product flow, and possible contamination pathways.

The prototype does not approve, reject, score, or rank applications. Human Thai FDA officers remain responsible for all regulatory decisions.

## Phase 2 Deferred

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

No real Thai FDA records, confidential business data, applicant data, official logos, or real facility layouts are included. The Phase 3, Phase 4, and Phase 5 components are synthetic-data prototypes and do not claim real-world validation.

## Scope

- Synthetic annotation schema for simplified food manufacturing floor plans.
- Spatial feature extraction for rooms, objects, and flow paths.
- Explainable GMP-oriented rule engine.
- Transparent risk report output in JSON.
- Heatmap generation for officer review.
- Synthetic computer vision-assisted floor-plan extraction demonstration.
- Synthetic revision-risk model training and prediction demonstration.
- Synthetic Thai FDA officer workflow simulation with audit log and reports.
- Streamlit demonstration app.
- Pytest coverage for core components.

## Data Governance

Only synthetic data is included. Do not commit real Thai FDA records, applicant names, addresses, license numbers, signatures, official logos, confidential business data, or non-public facility layouts.

## Install

```bash
pip install -e .
```

## Run CLI Demo

```bash
python scripts/run_screening.py \
  --annotation data/sample_synthetic/annotation_simple_factory.json \
  --rules configs/rules_gmp_thai_fda.yaml \
  --output outputs/demo_report.json \
  --heatmap outputs/demo_heatmap.png
```

## Run Phase 3 Synthetic CV Demo

```bash
python scripts/run_cv_demo.py \
  --annotation data/sample_synthetic/annotation_simple_factory.json \
  --image-output outputs/synthetic_floorplan.png \
  --detected-output outputs/synthetic_cv_detected_annotation.json
```

## Run Phase 4 Synthetic ML Demo

```bash
python scripts/generate_synthetic_training_data.py \
  --output outputs/synthetic_revision_training.csv \
  --count 160

python scripts/train_revision_risk_model.py \
  --training-data outputs/synthetic_revision_training.csv \
  --model-output outputs/synthetic_revision_risk_model.pkl \
  --metrics-output outputs/synthetic_revision_risk_metrics.json

python scripts/predict_revision_risk.py \
  --model outputs/synthetic_revision_risk_model.pkl \
  --screening-report outputs/demo_report.json \
  --output outputs/synthetic_revision_risk_prediction.json
```

## Run Phase 5 Workflow Demo

```bash
python scripts/run_workflow_demo.py \
  --annotation data/sample_synthetic/annotation_simple_factory.json \
  --rules configs/rules_gmp_thai_fda.yaml \
  --markdown-output outputs/synthetic_officer_report.md \
  --json-output outputs/synthetic_officer_report.json \
  --audit-output outputs/synthetic_audit_log.json \
  --model outputs/synthetic_revision_risk_model.pkl
```

## Run Streamlit App

```bash
pip install -e ".[app]"
streamlit run src/floorplan_ai/app/streamlit_app.py
```

## Expected Demo Findings

The synthetic sample intentionally includes:

- Toilet too close to a production area.
- Waste flow crossing product flow.
- Raw material storage too close to finished product storage.

Additional advisory review flags may be generated depending on rule thresholds.

## Repository Structure

```text
thai-fda-floorplan-ai/
  configs/
  data/sample_synthetic/
  docs/
  scripts/
  src/floorplan_ai/
  tests/
```

## Limitations

This prototype uses simplified geometric annotations, deterministic rules, synthetic computer vision helpers, synthetic model training data, and synthetic workflow records. It does not evaluate all Thai FDA or GMP requirements, validate against real Thai FDA records, or replace officer judgment. Real Thai FDA de-identified data and expert annotation are required before any validation, pilot, or operational use.
