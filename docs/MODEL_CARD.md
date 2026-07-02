# Model Card

## System Type

This repository contains an explainable rule-based screening system plus synthetic Phase 3, Phase 4, and Phase 5 demonstration components. The Phase 4 classifier is trained only on generated synthetic rows.

## Phase 2 Deferred

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

## Intended Use

Advisory pre-screening support for Thai FDA food manufacturing floor-plan review. The system highlights spatial conditions that may require human officer review.

## Out-of-Scope Use

The system must not be used to approve, reject, rank, or automatically decide applications. It must not be used with real Thai FDA data without a formally approved data governance process.

## Inputs

- Synthetic annotation JSON.
- Optional floor-plan image for heatmap background.
- Rule YAML configuration.
- Synthetic training CSV for the Phase 4 model.
- Officer comments and override notes for the Phase 5 simulation.

## Outputs

- Advisory JSON report.
- Risk findings with explanations and recommended human review actions.
- Heatmap PNG.
- Synthetic CV detected annotation JSON.
- Synthetic revision-risk class probabilities and feature contributors.
- Officer-facing Markdown and JSON reports.
- Audit log.

## Limitations

- Uses simplified geometry.
- Depends on annotation quality.
- Does not parse CAD or PDF drawings.
- Does not cover all GMP or Thai FDA requirements.
- Does not replace site inspection, document review, or officer judgment.
- Does not claim real-world model performance or validation.
- Does not use real Thai FDA records.

## Human Oversight

All findings require officer review. Reports explicitly state that human Thai FDA officers remain responsible for regulatory decisions.
