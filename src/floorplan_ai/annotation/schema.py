"""Pydantic schema for synthetic floor-plan annotations."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


RoomType = Literal[
    "production_area",
    "raw_material_storage",
    "finished_product_storage",
    "packaging_area",
    "washing_area",
    "toilet",
    "waste_area",
    "corridor",
    "unknown",
    "unlabeled_room",
]

ObjectType = Literal[
    "door",
    "window",
    "sink",
    "handwashing_point",
    "drain",
    "equipment",
]

FlowType = Literal[
    "personnel_flow",
    "raw_material_flow",
    "product_flow",
    "waste_flow",
]


class StrictModel(BaseModel):
    """Base model with stable validation behavior."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Point(StrictModel):
    x: float
    y: float


class BoundingBox(StrictModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @model_validator(mode="after")
    def validate_bounds(self) -> "BoundingBox":
        if self.x_max <= self.x_min:
            raise ValueError("x_max must be greater than x_min")
        if self.y_max <= self.y_min:
            raise ValueError("y_max must be greater than y_min")
        return self


class Polygon(StrictModel):
    points: list[Point] = Field(min_length=3)

    @field_validator("points")
    @classmethod
    def validate_unique_points(cls, value: list[Point]) -> list[Point]:
        unique_points = {(point.x, point.y) for point in value}
        if len(unique_points) < 3:
            raise ValueError("polygon must contain at least three unique points")
        return value


class FloorPlanObject(StrictModel):
    object_id: str = Field(min_length=1)
    object_type: ObjectType
    bbox: BoundingBox | None = None
    polygon: Polygon | None = None
    room_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_geometry(self) -> "FloorPlanObject":
        if self.bbox is None and self.polygon is None:
            raise ValueError("object must have bbox or polygon geometry")
        return self


class Room(StrictModel):
    room_id: str = Field(min_length=1)
    room_type: RoomType
    polygon: Polygon
    metadata: dict[str, Any] = Field(default_factory=dict)


class FlowPath(StrictModel):
    flow_id: str = Field(min_length=1)
    flow_type: FlowType
    points: list[Point] = Field(min_length=2)
    related_object_ids: list[str] = Field(default_factory=list)


class FloorPlanAnnotation(StrictModel):
    annotation_id: str = Field(min_length=1)
    version: str = Field(default="1.0", min_length=1)
    image_width: int = Field(gt=0)
    image_height: int = Field(gt=0)
    advisory_only: bool = True
    rooms: list[Room] = Field(default_factory=list)
    objects: list[FloorPlanObject] = Field(default_factory=list)
    flows: list[FlowPath] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_annotation(self) -> "FloorPlanAnnotation":
        if not self.advisory_only:
            raise ValueError("floor-plan screening annotations must be advisory_only")

        room_ids = [room.room_id for room in self.rooms]
        object_ids = [obj.object_id for obj in self.objects]
        flow_ids = [flow.flow_id for flow in self.flows]

        for label, values in {
            "room_id": room_ids,
            "object_id": object_ids,
            "flow_id": flow_ids,
        }.items():
            if len(values) != len(set(values)):
                raise ValueError(f"duplicate {label} values are not allowed")

        known_room_ids = set(room_ids)
        for obj in self.objects:
            if obj.room_id is not None and obj.room_id not in known_room_ids:
                raise ValueError(f"object {obj.object_id} references unknown room_id")

        known_related_ids = set(room_ids) | set(object_ids)
        for flow in self.flows:
            missing_ids = [item for item in flow.related_object_ids if item not in known_related_ids]
            if missing_ids:
                raise ValueError(f"flow {flow.flow_id} references unknown related ids")

        return self
