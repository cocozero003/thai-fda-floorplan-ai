# Model Card

## System Type

This Phase 1 prototype is not a trained predictive model. It is an explainable rule-based screening system using synthetic floor-plan annotations and configurable GMP-oriented rules.

## Intended Use

Advisory pre-screening support for Thai FDA food manufacturing floor-plan review. The system highlights spatial conditions that may require human officer review.

## Out-of-Scope Use

The system must not be used to approve, reject, rank, or automatically decide applications. It must not be used with real Thai FDA data without a formally approved data governance process.

## Inputs

- Synthetic annotation JSON.
- Optional floor-plan image for heatmap background.
- Rule YAML configuration.

## Outputs

- Advisory JSON report.
- Risk findings with explanations and recommended human review actions.
- Heatmap PNG.

## Limitations

- Uses simplified geometry.
- Depends on annotation quality.
- Does not parse CAD or PDF drawings.
- Does not cover all GMP or Thai FDA requirements.
- Does not replace site inspection, document review, or officer judgment.

## Human Oversight

All findings require officer review. Reports explicitly state that human Thai FDA officers remain responsible for regulatory decisions.
