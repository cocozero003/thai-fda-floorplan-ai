# Explainable Regulatory Health Informatics for Thai FDA Food Manufacturing Floor-Plan Pre-Screening

This repository contains a Phase 1 research prototype for GMP-oriented food manufacturing floor-plan pre-screening. It is designed as an advisory decision-support tool that helps Thai FDA officers review synthetic floor-plan annotations for spatial layout risks such as unsafe adjacency, crossing flows, insufficient sanitation access, toilet proximity to production areas, waste flow crossing product flow, and possible contamination pathways.

The prototype does not approve, reject, score, or rank applications. Human Thai FDA officers remain responsible for all regulatory decisions.

## Scope

- Synthetic annotation schema for simplified food manufacturing floor plans.
- Spatial feature extraction for rooms, objects, and flow paths.
- Explainable GMP-oriented rule engine.
- Transparent risk report output in JSON.
- Heatmap generation for officer review.
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

This Phase 1 prototype uses simplified geometric annotations and deterministic rules. It does not parse engineering drawings, infer room labels from images, evaluate all Thai FDA or GMP requirements, or replace officer judgment. Future phases may add human-reviewed datasets, computer vision assistance, uncertainty calibration, Thai-language reporting, and integration testing with controlled non-production workflows.
