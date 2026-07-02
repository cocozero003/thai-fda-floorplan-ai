# Annotation Guide

## Purpose

The annotation schema captures simplified floor-plan geometry for advisory GMP-based screening. It supports room polygons, object bounding boxes or polygons, and flow paths.

## Room Types

- `production_area`
- `raw_material_storage`
- `finished_product_storage`
- `packaging_area`
- `washing_area`
- `toilet`
- `waste_area`
- `corridor`
- `unknown`
- `unlabeled_room`

## Object Types

- `door`
- `window`
- `sink`
- `handwashing_point`
- `drain`
- `equipment`

## Flow Types

- `personnel_flow`
- `raw_material_flow`
- `product_flow`
- `waste_flow`

## Geometry Guidance

Use simple plan-coordinate units. Room polygons should contain at least three unique points. Object bounding boxes must have valid minimum and maximum coordinates. Flow paths should represent directional movement with at least two points.

## Governance Reminder

Use only synthetic data in this repository. Do not include real applicants, addresses, license numbers, signatures, official logos, or confidential business data.
