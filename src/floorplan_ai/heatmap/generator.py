"""Generate transparent advisory risk heatmaps."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw

from floorplan_ai.annotation.schema import FloorPlanAnnotation, Polygon
from floorplan_ai.rules.rule_engine import RiskFinding


RISK_COLORS = {
    "high": (220, 40, 40, 105),
    "medium": (245, 190, 40, 105),
    "uncertain": (245, 190, 40, 105),
    "review": (245, 190, 40, 90),
    "low": (45, 150, 70, 85),
}


def _polygon_points(polygon: Polygon) -> list[tuple[float, float]]:
    return [(point.x, point.y) for point in polygon.points]


def _severity_color(severity: str) -> tuple[int, int, int, int]:
    return RISK_COLORS.get(severity, RISK_COLORS["low"])


def _rooms_for_finding(annotation: FloorPlanAnnotation, finding: RiskFinding) -> list[tuple[str, Polygon]]:
    rooms: list[tuple[str, Polygon]] = []
    room_by_id = {room.room_id: room for room in annotation.rooms}
    object_room_lookup = {obj.object_id: obj.room_id for obj in annotation.objects}

    for related_id in finding.related_object_ids:
        if related_id in room_by_id:
            room = room_by_id[related_id]
            rooms.append((room.room_id, room.polygon))
            continue
        room_id = object_room_lookup.get(related_id)
        if room_id is not None and room_id in room_by_id:
            room = room_by_id[room_id]
            rooms.append((room.room_id, room.polygon))

    seen: set[str] = set()
    unique_rooms: list[tuple[str, Polygon]] = []
    for room_id, polygon in rooms:
        if room_id not in seen:
            unique_rooms.append((room_id, polygon))
            seen.add(room_id)
    return unique_rooms


def _draw_room_outlines(draw: ImageDraw.ImageDraw, annotation: FloorPlanAnnotation) -> None:
    for room in annotation.rooms:
        draw.polygon(_polygon_points(room.polygon), outline=(80, 80, 80, 255), width=2)
        centroid_x = sum(point.x for point in room.polygon.points) / len(room.polygon.points)
        centroid_y = sum(point.y for point in room.polygon.points) / len(room.polygon.points)
        draw.text((centroid_x - 30, centroid_y - 6), room.room_type, fill=(30, 30, 30, 255))


def _draw_finding_labels(
    draw: ImageDraw.ImageDraw,
    annotation: FloorPlanAnnotation,
    finding: RiskFinding,
    polygons: Iterable[Polygon],
) -> None:
    for polygon in polygons:
        centroid_x = sum(point.x for point in polygon.points) / len(polygon.points)
        centroid_y = sum(point.y for point in polygon.points) / len(polygon.points)
        label = finding.rule_id
        draw.rectangle((centroid_x - 4, centroid_y - 13, centroid_x + 76, centroid_y + 5), fill=(255, 255, 255, 180))
        draw.text((centroid_x, centroid_y - 12), label, fill=(0, 0, 0, 255))

    for flow in annotation.flows:
        if flow.flow_id in finding.related_object_ids and len(flow.points) >= 2:
            midpoint = flow.points[len(flow.points) // 2]
            draw.text((midpoint.x + 4, midpoint.y + 4), finding.rule_id, fill=(0, 0, 0, 255))


def generate_heatmap(
    annotation: FloorPlanAnnotation,
    risk_findings: list[RiskFinding],
    image_path: str | Path | None = None,
    output_path: str | Path = "outputs/heatmap.png",
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if image_path is not None:
        base = Image.open(image_path).convert("RGBA").resize((annotation.image_width, annotation.image_height))
    else:
        base = Image.new("RGBA", (annotation.image_width, annotation.image_height), (248, 248, 246, 255))

    outline_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
    outline_draw = ImageDraw.Draw(outline_layer)
    _draw_room_outlines(outline_draw, annotation)

    overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for finding in risk_findings:
        related_rooms = _rooms_for_finding(annotation, finding)
        polygons = [polygon for _, polygon in related_rooms]
        if not polygons and annotation.rooms:
            polygons = [annotation.rooms[0].polygon]

        for polygon in polygons:
            overlay_draw.polygon(_polygon_points(polygon), fill=_severity_color(finding.severity))
        _draw_finding_labels(overlay_draw, annotation, finding, polygons)

    combined = Image.alpha_composite(base, outline_layer)
    combined = Image.alpha_composite(combined, overlay)
    combined.convert("RGBA").save(output, format="PNG")
    return output
