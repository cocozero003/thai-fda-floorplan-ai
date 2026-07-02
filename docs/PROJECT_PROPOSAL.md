# Project Proposal

## Title

Explainable Regulatory Health Informatics for Thai FDA Food Manufacturing Floor-Plan Pre-Screening

## Context

Thai FDA officers review food manufacturing facility information as part of GMP-based regulatory oversight. Facility floor plans can contain spatial layout risks that are relevant to food safety review, including poor zoning, unsafe adjacency, crossing material flows, insufficient sanitation access, toilet proximity to production areas, waste routes crossing product routes, and possible contamination pathways.

## Phase 1 Objective

This Phase 1 prototype demonstrates an explainable, rule-based decision-support workflow using synthetic annotations. It helps officers identify layout conditions that may deserve manual review. It does not approve or reject applications.

## Prototype Components

- Synthetic floor-plan annotation schema.
- Spatial feature extraction for rooms, objects, and flows.
- GMP-oriented advisory rule configuration.
- Explainable rule engine with officer-review findings.
- Heatmap visualization.
- CLI demonstration and Streamlit app.
- Tests using only synthetic data.

## Human-in-the-Loop Use

All findings require officer review. The system is intended to support consistent pre-screening and transparent discussion, not final regulatory judgment. Thai FDA officers remain responsible for all decisions and interpretations.

## Future Phases

- Expand annotation guidelines with officer-reviewed synthetic and training examples.
- Add controlled data governance workflows before any real-world pilot.
- Evaluate inter-rater agreement and rule usefulness.
- Explore computer vision assistance for drawing interpretation.
- Add Thai-language reporting after policy and terminology review.
