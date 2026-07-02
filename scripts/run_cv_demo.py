"""Run the Phase 3 synthetic computer vision demonstration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.cv.annotation_converter import detections_to_annotation
from floorplan_ai.cv.detector import detect_synthetic_floorplan
from floorplan_ai.cv.preprocess import preprocess_image
from generate_synthetic_floorplan_image import generate_synthetic_floorplan_image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run synthetic CV floor-plan extraction demo.")
    parser.add_argument("--annotation", required=True, help="Path to synthetic annotation JSON.")
    parser.add_argument("--image-output", required=True, help="Path to write generated PNG.")
    parser.add_argument("--detected-output", required=True, help="Path to write detected annotation JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = FloorPlanAnnotation.model_validate_json(Path(args.annotation).read_text(encoding="utf-8"))
    image_path = generate_synthetic_floorplan_image(source, args.image_output)
    preprocessed = preprocess_image(image_path)
    detections = detect_synthetic_floorplan(image_path)
    detected_annotation = detections_to_annotation(
        detections,
        preprocessed["width"],
        preprocessed["height"],
        annotation_id="synthetic-cv-demo-detected",
    )

    output = Path(args.detected_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(detected_annotation.model_dump(), indent=2), encoding="utf-8")

    print("Phase 3 synthetic CV demo complete.")
    print("Synthetic image written to " + str(image_path))
    print("Detected advisory annotation written to " + str(output))
    print("Not trained on real Thai FDA data. Advisory demonstration only.")


if __name__ == "__main__":
    main()
