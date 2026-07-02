# Phase 3 Computer Vision Prototype

Phase 3 is a synthetic computer vision-assisted floor-plan extraction demonstration.

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

## What It Does

- Generates a synthetic floor-plan PNG from `FloorPlanAnnotation` JSON.
- Preprocesses the synthetic image with grayscale and threshold steps.
- Detects color-coded synthetic rooms and objects.
- Converts detections back into `FloorPlanAnnotation` format.

## What It Does Not Do

- It is not trained on real Thai FDA records.
- It does not parse real applicant drawings.
- It does not validate room or object detection performance in the real world.
- It does not approve or reject applications.

## Demo

```bash
python scripts/run_cv_demo.py \
  --annotation data/sample_synthetic/annotation_simple_factory.json \
  --image-output outputs/synthetic_floorplan.png \
  --detected-output outputs/synthetic_cv_detected_annotation.json
```

The output annotation is advisory and synthetic only.
