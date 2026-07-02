# Data Governance

## Data Classification

This repository contains synthetic data only. Synthetic annotations are designed for prototype testing and do not represent real Thai FDA applications, real facilities, or confidential business information.

## Phase 2 Deferred

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

Phase 3 computer vision outputs, Phase 4 revision-risk model outputs, and Phase 5 workflow reports are synthetic demonstrations. They must not be described as validated against real Thai FDA records.

## Prohibited Data

Do not commit:

- Real Thai FDA application records.
- Applicant names.
- Addresses or map coordinates.
- License numbers.
- Signatures.
- Official logos.
- Confidential business data.
- Real facility layouts without a formally approved governance process.

## Advisory-Only Controls

Generated reports must state that they are advisory decision support only. The system must not approve, reject, rank, or automatically decide regulatory outcomes.

## Human Review

Thai FDA officers remain responsible for regulatory decisions. Findings should be treated as prompts for manual review, clarification, or site-specific interpretation.

## Synthetic Data Use

The sample annotation in `data/sample_synthetic/` is intentionally simplified and includes known synthetic risks for testing:

- Toilet near production area.
- Waste flow crossing product flow.
- Raw material storage close to finished product storage.
