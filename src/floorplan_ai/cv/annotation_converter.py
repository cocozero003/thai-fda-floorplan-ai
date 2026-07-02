"""Convert synthetic detector output into annotation schema objects."""

from __future__ import annotations

from floorplan_ai.annotation.schema import (
    BoundingBox,
    FloorPlanAnnotation,
    FloorPlanObject,
    Point,
    Polygon,
    Room,
)
from floorplan_ai.cv.detector import Detection


def _box_polygon(box: tuple[int, int, int, int]) -> Polygon:
    x_min, y_min, x_max, y_max = box
    return Polygon(
        points=[
            Point(x=x_min, y=y_min),
            Point(x=x_max, y=y_min),
            Point(x=x_max, y=y_max),
            Point(x=x_min, y=y_max),
        ]
    )


def _contains(room: Room, box: tuple[int, int, int, int]) -> bool:
    x_min, y_min, x_max, y_max = box
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    xs = [point.x for point in room.polygon.points]
    ys = [point.y for point in room.polygon.points]
    return min(xs) <= center_x <= max(xs) and min(ys) <= center_y <= max(ys)


def detections_to_annotation(
    detections: list[Detection],
    image_width: int,
    image_height: int,
    annotation_id: str = "synthetic-cv-detected-annotation",
) -> FloorPlanAnnotation:
    """Build a synthetic FloorPlanAnnotation from color detector output."""

    rooms: list[Room] = []
    objects: list[FloorPlanObject] = []
    room_counts: dict[str, int] = {}
    object_counts: dict[str, int] = {}

    for detection in detections:
        if detection.category != "room":
            continue
        room_counts[detection.label] = room_counts.get(detection.label, 0) + 1
        rooms.append(
            Room(
                room_id=f"cv-room-{detection.label}-{room_counts[detection.label]}",
                room_type=detection.label,
                polygon=_box_polygon(detection.bbox),
                metadata={
                    "source": detection.source,
                    "confidence": detection.confidence,
                    "synthetic_data_only": True,
                },
            )
        )

    for detection in detections:
        if detection.category != "object":
            continue
        object_counts[detection.label] = object_counts.get(detection.label, 0) + 1
        room_id = next((room.room_id for room in rooms if _contains(room, detection.bbox)), None)
        x_min, y_min, x_max, y_max = detection.bbox
        objects.append(
            FloorPlanObject(
                object_id=f"cv-object-{detection.label}-{object_counts[detection.label]}",
                object_type=detection.label,
                bbox=BoundingBox(x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max),
                room_id=room_id,
                metadata={
                    "source": detection.source,
                    "confidence": detection.confidence,
                    "synthetic_data_only": True,
                },
            )
        )

    return FloorPlanAnnotation(
        annotation_id=annotation_id,
        image_width=image_width,
        image_height=image_height,
        advisory_only=True,
        rooms=rooms,
        objects=objects,
        flows=[],
        metadata={
            "data_classification": "synthetic",
            "contains_real_thai_fda_data": False,
            "phase": "Phase 3 synthetic computer vision prototype",
            "warning": "Not trained on real Thai FDA data. Advisory demonstration only.",
        },
    )
