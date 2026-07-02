from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.cv.annotation_converter import detections_to_annotation
from floorplan_ai.cv.detector import detect_synthetic_floorplan
from scripts.generate_synthetic_floorplan_image import generate_synthetic_floorplan_image


def test_detect_synthetic_floorplan_and_convert_to_annotation(tmp_path: Path) -> None:
    annotation = FloorPlanAnnotation.model_validate_json(
        Path("data/sample_synthetic/annotation_simple_factory.json").read_text(encoding="utf-8")
    )
    image_path = generate_synthetic_floorplan_image(annotation, tmp_path / "floorplan.png")

    detections = detect_synthetic_floorplan(image_path)
    detected_annotation = detections_to_annotation(
        detections,
        annotation.image_width,
        annotation.image_height,
        annotation_id="test-detected",
    )

    assert any(detection.category == "room" for detection in detections)
    assert any(detection.category == "object" for detection in detections)
    assert detected_annotation.advisory_only is True
    assert detected_annotation.metadata["contains_real_thai_fda_data"] is False
    assert len(detected_annotation.rooms) >= 5
