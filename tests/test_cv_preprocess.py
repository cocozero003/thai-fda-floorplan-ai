from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.cv.preprocess import preprocess_image
from scripts.generate_synthetic_floorplan_image import generate_synthetic_floorplan_image


def test_preprocess_image_returns_synthetic_derivatives(tmp_path: Path) -> None:
    annotation = FloorPlanAnnotation.model_validate_json(
        Path("data/sample_synthetic/annotation_simple_factory.json").read_text(encoding="utf-8")
    )
    image_path = generate_synthetic_floorplan_image(annotation, tmp_path / "floorplan.png")

    result = preprocess_image(image_path)

    assert result["width"] == annotation.image_width
    assert result["height"] == annotation.image_height
    assert result["synthetic_data_only"] is True
    assert result["binary"].mode == "L"
