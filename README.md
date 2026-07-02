
# Thai FDA Floorplan AI

Explainable regulatory health informatics prototype for Thai FDA food manufacturing facility floor-plan pre-screening.

## Purpose

This project develops a human-in-the-loop decision-support system for GMP-based food manufacturing floor-plan review. It is intended to help regulatory officers identify possible spatial risks such as poor zoning, unsafe adjacency, crossing flow, insufficient sanitation access, and contamination pathways.

The system is advisory only. It does not approve or reject applications.

## Core modules

1. Preprocessing
2. Annotation schema
3. Spatial feature extraction
4. GMP rule engine
5. Risk heatmap generation
6. Evaluation against expert labels
7. Officer-facing prototype app

## Development phases

### Phase 1
Rule-based prototype with manual or semi-automatic annotation.

### Phase 2
Computer vision-assisted extraction of rooms, doors, windows, sinks, toilets, storage zones, production zones, and flow paths.

### Phase 3
Predictive model for revision-risk scoring using historical Thai FDA outcomes.

## Data governance

Do not commit raw floor plans, applicant names, addresses, license numbers, or confidential business data.
Use only synthetic examples in this repository.
EOF
