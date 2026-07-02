import json
from pathlib import Path

import pytest

from floorplan_ai.annotation.schema import BoundingBox, FloorPlanAnnotation, Polygon


SAMPLE = Path("data/sample_synthetic/annotation_simple_factory.json")


def test_loads_synthetic_annotation() -> None:
    annotation = FloorPlanAnnotation.model_validate_json(SAMPLE.read_text(encoding="utf-8"))

    assert annotation.annotation_id == "synthetic-simple-factory-001"
    assert annotation.advisory_only is True
    assert {room.room_type for room in annotation.rooms} >= {
        "production_area",
        "raw_material_storage",
        "finished_product_storage",
        "packaging_area",
        "washing_area",
        "toilet",
        "waste_area",
        "corridor",
    }
    assert {flow.flow_type for flow in annotation.flows} == {
        "personnel_flow",
        "raw_material_flow",
        "product_flow",
        "waste_flow",
    }


def test_rejects_non_advisory_annotation() -> None:
    payload = json.loads(SAMPLE.read_text(encoding="utf-8"))
    payload["advisory_only"] = False

    with pytest.raises(ValueError, match="advisory_only"):
        FloorPlanAnnotation.model_validate(payload)


def test_validates_geometry() -> None:
    with pytest.raises(ValueError):
        BoundingBox(x_min=10, y_min=0, x_max=5, y_max=10)

    with pytest.raises(ValueError):
        Polygon(points=[{"x": 1, "y": 1}, {"x": 1, "y": 1}, {"x": 1, "y": 1}])
