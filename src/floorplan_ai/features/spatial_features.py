"""Spatial features for explainable floor-plan risk screening."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from itertools import combinations
from typing import Any

from floorplan_ai.annotation.schema import (
    BoundingBox,
    FloorPlanAnnotation,
    FlowPath,
    FloorPlanObject,
    Point,
    Polygon,
    Room,
)


def polygon_area(polygon: Polygon) -> float:
    points = polygon.points
    area = 0.0
    for current, nxt in zip(points, points[1:] + points[:1]):
        area += current.x * nxt.y - nxt.x * current.y
    return abs(area) / 2.0


def polygon_centroid(polygon: Polygon) -> Point:
    points = polygon.points
    signed_area = 0.0
    centroid_x = 0.0
    centroid_y = 0.0

    for current, nxt in zip(points, points[1:] + points[:1]):
        cross = current.x * nxt.y - nxt.x * current.y
        signed_area += cross
        centroid_x += (current.x + nxt.x) * cross
        centroid_y += (current.y + nxt.y) * cross

    signed_area *= 0.5
    if math.isclose(signed_area, 0.0):
        avg_x = sum(point.x for point in points) / len(points)
        avg_y = sum(point.y for point in points) / len(points)
        return Point(x=avg_x, y=avg_y)

    return Point(x=centroid_x / (6.0 * signed_area), y=centroid_y / (6.0 * signed_area))


def bbox_center(bbox: BoundingBox) -> Point:
    return Point(x=(bbox.x_min + bbox.x_max) / 2.0, y=(bbox.y_min + bbox.y_max) / 2.0)


def euclidean_distance(point_a: Point, point_b: Point) -> float:
    return math.hypot(point_a.x - point_b.x, point_a.y - point_b.y)


def _orientation(a: Point, b: Point, c: Point) -> int:
    value = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if math.isclose(value, 0.0):
        return 0
    return 1 if value > 0 else 2


def _on_segment(a: Point, b: Point, c: Point) -> bool:
    return (
        min(a.x, c.x) <= b.x <= max(a.x, c.x)
        and min(a.y, c.y) <= b.y <= max(a.y, c.y)
    )


def line_segments_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    orientation_1 = _orientation(p1, q1, p2)
    orientation_2 = _orientation(p1, q1, q2)
    orientation_3 = _orientation(p2, q2, p1)
    orientation_4 = _orientation(p2, q2, q1)

    if orientation_1 != orientation_2 and orientation_3 != orientation_4:
        return True

    if orientation_1 == 0 and _on_segment(p1, p2, q1):
        return True
    if orientation_2 == 0 and _on_segment(p1, q2, q1):
        return True
    if orientation_3 == 0 and _on_segment(p2, p1, q2):
        return True
    if orientation_4 == 0 and _on_segment(p2, q1, q2):
        return True
    return False


def object_count_by_class(annotation: FloorPlanAnnotation) -> dict[str, int]:
    counts = Counter(obj.object_type for obj in annotation.objects)
    counts.update(room.room_type for room in annotation.rooms)
    return dict(counts)


def room_area_by_type(annotation: FloorPlanAnnotation) -> dict[str, float]:
    areas: dict[str, float] = defaultdict(float)
    for room in annotation.rooms:
        areas[room.room_type] += polygon_area(room.polygon)
    return dict(areas)


def _entity_center(entity: Room | FloorPlanObject) -> Point:
    if isinstance(entity, Room):
        return polygon_centroid(entity.polygon)
    if entity.polygon is not None:
        return polygon_centroid(entity.polygon)
    if entity.bbox is not None:
        return bbox_center(entity.bbox)
    raise ValueError("entity has no geometry")


def _bbox_to_polygon(bbox: BoundingBox) -> Polygon:
    return Polygon(
        points=[
            Point(x=bbox.x_min, y=bbox.y_min),
            Point(x=bbox.x_max, y=bbox.y_min),
            Point(x=bbox.x_max, y=bbox.y_max),
            Point(x=bbox.x_min, y=bbox.y_max),
        ]
    )


def _entity_polygon(entity: Room | FloorPlanObject) -> Polygon:
    if isinstance(entity, Room):
        return entity.polygon
    if entity.polygon is not None:
        return entity.polygon
    if entity.bbox is not None:
        return _bbox_to_polygon(entity.bbox)
    raise ValueError("entity has no geometry")


def _point_to_segment_distance(point: Point, segment_start: Point, segment_end: Point) -> float:
    dx = segment_end.x - segment_start.x
    dy = segment_end.y - segment_start.y
    if math.isclose(dx, 0.0) and math.isclose(dy, 0.0):
        return euclidean_distance(point, segment_start)

    projection = ((point.x - segment_start.x) * dx + (point.y - segment_start.y) * dy) / (dx * dx + dy * dy)
    projection = max(0.0, min(1.0, projection))
    closest = Point(x=segment_start.x + projection * dx, y=segment_start.y + projection * dy)
    return euclidean_distance(point, closest)


def _point_in_polygon(point: Point, polygon: Polygon) -> bool:
    inside = False
    points = polygon.points
    j = len(points) - 1
    for i, current in enumerate(points):
        previous = points[j]
        intersects = ((current.y > point.y) != (previous.y > point.y)) and (
            point.x
            < (previous.x - current.x) * (point.y - current.y) / ((previous.y - current.y) or 1e-12)
            + current.x
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def _polygon_segments(polygon: Polygon) -> list[tuple[Point, Point]]:
    return list(zip(polygon.points, polygon.points[1:] + polygon.points[:1]))


def _polygon_distance(polygon_a: Polygon, polygon_b: Polygon) -> float:
    segments_a = _polygon_segments(polygon_a)
    segments_b = _polygon_segments(polygon_b)

    if any(line_segments_intersect(a1, a2, b1, b2) for a1, a2 in segments_a for b1, b2 in segments_b):
        return 0.0
    if _point_in_polygon(polygon_a.points[0], polygon_b) or _point_in_polygon(polygon_b.points[0], polygon_a):
        return 0.0

    distances: list[float] = []
    for point in polygon_a.points:
        distances.extend(_point_to_segment_distance(point, start, end) for start, end in segments_b)
    for point in polygon_b.points:
        distances.extend(_point_to_segment_distance(point, start, end) for start, end in segments_a)
    return min(distances)


def _entity_type(entity: Room | FloorPlanObject) -> str:
    return entity.room_type if isinstance(entity, Room) else entity.object_type


def _entity_id(entity: Room | FloorPlanObject) -> str:
    return entity.room_id if isinstance(entity, Room) else entity.object_id


def _entities_by_class(annotation: FloorPlanAnnotation, class_name: str) -> list[Room | FloorPlanObject]:
    entities: list[Room | FloorPlanObject] = []
    entities.extend(room for room in annotation.rooms if room.room_type == class_name)
    entities.extend(obj for obj in annotation.objects if obj.object_type == class_name)
    return entities


def minimum_distance_between_classes(
    annotation: FloorPlanAnnotation,
    class_a: str,
    class_b: str,
) -> dict[str, Any] | None:
    entities_a = _entities_by_class(annotation, class_a)
    entities_b = _entities_by_class(annotation, class_b)
    best: dict[str, Any] | None = None

    for entity_a in entities_a:
        for entity_b in entities_b:
            if _entity_id(entity_a) == _entity_id(entity_b):
                continue
            center_a = _entity_center(entity_a)
            center_b = _entity_center(entity_b)
            distance = _polygon_distance(_entity_polygon(entity_a), _entity_polygon(entity_b))
            if best is None or distance < best["distance"]:
                best = {
                    "class_a": class_a,
                    "class_b": class_b,
                    "object_id_a": _entity_id(entity_a),
                    "object_id_b": _entity_id(entity_b),
                    "distance": distance,
                    "center_a": center_a.model_dump(),
                    "center_b": center_b.model_dump(),
                }

    return best


def _flow_segments(flow: FlowPath) -> list[tuple[Point, Point]]:
    return list(zip(flow.points, flow.points[1:]))


def detect_flow_intersections(annotation: FloorPlanAnnotation) -> list[dict[str, Any]]:
    intersections: list[dict[str, Any]] = []
    for flow_a, flow_b in combinations(annotation.flows, 2):
        for segment_index_a, segment_a in enumerate(_flow_segments(flow_a)):
            for segment_index_b, segment_b in enumerate(_flow_segments(flow_b)):
                if line_segments_intersect(segment_a[0], segment_a[1], segment_b[0], segment_b[1]):
                    intersections.append(
                        {
                            "flow_id_a": flow_a.flow_id,
                            "flow_type_a": flow_a.flow_type,
                            "segment_index_a": segment_index_a,
                            "flow_id_b": flow_b.flow_id,
                            "flow_type_b": flow_b.flow_type,
                            "segment_index_b": segment_index_b,
                            "related_object_ids": sorted(
                                set(flow_a.related_object_ids) | set(flow_b.related_object_ids)
                            ),
                        }
                    )
    return intersections


def _all_minimum_distances(annotation: FloorPlanAnnotation) -> dict[str, dict[str, Any]]:
    classes = sorted(
        set(room.room_type for room in annotation.rooms)
        | set(obj.object_type for obj in annotation.objects)
    )
    distances: dict[str, dict[str, Any]] = {}
    for class_a, class_b in combinations(classes, 2):
        distance = minimum_distance_between_classes(annotation, class_a, class_b)
        if distance is not None:
            distances[f"{class_a}__{class_b}"] = distance
            reverse = dict(distance)
            reverse["class_a"] = class_b
            reverse["class_b"] = class_a
            reverse["object_id_a"] = distance["object_id_b"]
            reverse["object_id_b"] = distance["object_id_a"]
            reverse["center_a"] = distance["center_b"]
            reverse["center_b"] = distance["center_a"]
            distances[f"{class_b}__{class_a}"] = reverse
    return distances


def extract_spatial_features(annotation: FloorPlanAnnotation) -> dict[str, Any]:
    return {
        "annotation_id": annotation.annotation_id,
        "image_width": annotation.image_width,
        "image_height": annotation.image_height,
        "object_count_by_class": object_count_by_class(annotation),
        "room_area_by_type": room_area_by_type(annotation),
        "minimum_distances": _all_minimum_distances(annotation),
        "flow_intersections": detect_flow_intersections(annotation),
        "advisory_only": True,
    }
