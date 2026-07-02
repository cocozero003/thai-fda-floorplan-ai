# AGENTS.md

## Project
This repository implements an explainable regulatory health informatics prototype for Thai FDA food manufacturing facility floor-plan pre-screening.

## Main goal
Build a human-in-the-loop decision-support system that:
1. Ingests de-identified food manufacturing floor-plan PDFs/images.
2. Extracts or accepts annotated spatial elements.
3. Converts floor-plan elements into GMP-relevant spatial features.
4. Applies Thai FDA GMP-oriented rule checks.
5. Generates regulatory risk heatmaps.
6. Produces officer-reviewable reports.

## Safety and governance
- Do not include real applicant names, addresses, license numbers, signatures, or confidential facility information.
- Use synthetic or toy sample data in tests.
- Never commit raw regulatory documents.
- Treat the tool as advisory decision support only.
- Do not claim that the system automatically approves or rejects applications.

## Coding style
- Python 3.11+
- Use type hints.
- Prefer simple, readable code.
- Add docstrings for public functions.
- Use pytest for tests.
- Keep business logic separate from UI code.
- No emojis or icons in code, comments, logs, or documentation.

## Architecture
Use this package structure:

src/floorplan_ai/
  preprocessing/
  annotation/
  features/
  rules/
  models/
  heatmap/
  evaluation/
  app/

## Pull request rules
Every PR should include:
1. Summary
2. Files changed
3. Tests added or updated
4. Known limitations
5. Data governance note

## Testing
Run:
pytest

## Important
Prioritize Phase 1 prototype:
- annotation schema
- spatial feature extraction
- rule-based risk scoring
- heatmap generation
- evaluation against expert labels

Do not overbuild full deep learning until the rule-based prototype is stable.
EOF
