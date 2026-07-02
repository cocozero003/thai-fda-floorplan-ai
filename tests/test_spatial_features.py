from pathlib import Path

from floorplan_ai.annotation.schema import FloorPlanAnnotation, Point, Polygon
from floorplan_ai.features.spatial_features import (
    detect_flow_intersections,
    euclidean_distance,
    extract_spatial_features,
    line_segments_intersect,
    minimum_distance_between_classes,
    object_count_by_class,
    polygon_area,
    polygon_centroid,
    room_area_by_type,
)


SAMPLE = Path("data/sample_synthetic/annotation_simple_factory.json")


def _annotation() -> FloorPlanAnnotation:
    return FloorPlanAnnotation.model_validate_json(SAMPLE.read_text(encoding="utf-8"))


def test_polygon_area_and_centroid() -> None:
    polygon = Polygon(points=[Point(x=0, y=0), Point(x=10, y=0), Point(x=10, y=10), Point(x=0, y=10)])

    assert polygon_area(polygon) == 100
    centroid = polygon_centroid(polygon)
    assert centroid.x == 5
    assert centroid.y == 5


def test_distance_and_intersection_helpers() -> None:
    assert euclidean_distance(Point(x=0, y=0), Point(x=3, y=4)) == 5
    assert line_segments_intersect(Point(x=0, y=0), Point(x=10, y=10), Point(x=0, y=10), Point(x=10, y=0))
    assert not line_segments_intersect(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3))


def test_feature_extraction_identifies_synthetic_risks() -> None:
    annotation = _annotation()
    features = extract_spatial_features(annotation)

    assert object_count_by_class(annotation)["production_area"] == 1
    assert room_area_by_type(annotation)["production_area"] == 57200

    toilet_distance = minimum_distance_between_classes(annotation, "toilet", "production_area")
    assert toilet_distance is not None
    assert toilet_distance["distance"] < 200

    intersections = detect_flow_intersections(annotation)
    assert any(
        {item["flow_type_a"], item["flow_type_b"]} == {"waste_flow", "product_flow"}
        for item in intersections
    )
    assert features["advisory_only"] is True
