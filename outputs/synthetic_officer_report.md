# Synthetic Thai FDA Floor-Plan Pre-Screening Report

This report is advisory decision support only. It does not approve or reject any application.
Human Thai FDA officers remain responsible for all regulatory decisions.
Phase 2 is deferred. This repository currently uses synthetic data only.
Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

## Case

- Case ID: synthetic-workflow-case-001
- Annotation ID: synthetic-simple-factory-001
- Status: officer_review_required
- Officer comment: Synthetic officer comment for demo review.
- Officer override: No automatic decision. Officer review remains required.

## Rule-Based Findings

- Finding count: 6

### GMP-001: Toilet near production area

- Severity: high
- Confidence: 0.85
- Explanation: Advisory finding: toilet area is approximately 20.0 plan units from production area, below the review threshold of 80.0.
- Recommended officer review action: Confirm physical separation, door orientation, ventilation, handwashing access, and sanitation controls before any regulatory decision.

### GMP-002: Waste flow crossing product flow

- Severity: high
- Confidence: 0.9
- Explanation: Advisory finding: waste flow intersects product flow in the submitted floor-plan annotation.
- Recommended officer review action: Review routing, barriers, timing controls, and waste handling procedures with a human officer.

### GMP-003: Raw material storage close to finished product storage

- Severity: medium
- Confidence: 0.85
- Explanation: Advisory finding: raw material storage is approximately 20.0 plan units from finished product storage, below the review threshold of 130.0.
- Recommended officer review action: Verify segregation, directional flow, labeling, and handling controls.

### GMP-005: Window opening directly to production area

- Severity: review
- Confidence: 0.65
- Explanation: Advisory review flag: a window is approximately 0.0 plan units from production area.
- Recommended officer review action: Review screening, sealing, airflow, and contamination prevention controls.

### GMP-006: Waste area close to clean zone

- Severity: high
- Confidence: 0.85
- Explanation: Advisory finding: waste area is approximately 30.0 plan units from a clean zone, below the review threshold of 120.0.
- Recommended officer review action: Review waste segregation, removal path, containment, cleaning frequency, and physical separation.

### GMP-007: Unknown or unlabeled room near production

- Severity: uncertain
- Confidence: 0.55
- Explanation: Advisory uncertainty: an unknown or unlabeled room is approximately 20.0 plan units from production area.
- Recommended officer review action: Ask the applicant to clarify the room function and review the layout manually.

## Synthetic ML Revision-Risk Prediction

- Advisory revision-risk class: high
- Probability high: 0.992
- Probability low: 0.008
- Probability medium: 0.000
- Warning: Synthetic-data prototype only. No real Thai FDA records were used, and no real-world validation or operational performance is claimed.

## Audit Log

- 2026-07-02T13:05:49.770241+00:00 | system | session_created
- 2026-07-02T13:05:49.772357+00:00 | synthetic_officer | officer_input_recorded
- 2026-07-02T13:05:49.772357+00:00 | system | rule_screening_started
- 2026-07-02T13:05:49.812991+00:00 | system | rule_screening_completed
- 2026-07-02T13:05:49.812991+00:00 | system | synthetic_ml_prediction_started
- 2026-07-02T13:05:49.842787+00:00 | system | synthetic_ml_prediction_completed
