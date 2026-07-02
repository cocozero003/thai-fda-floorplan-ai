"""Generate a synthetic floor-plan PNG from synthetic annotation JSON."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.cv.detector import OBJECT_COLORS, ROOM_COLORS


def _polygon_points(points: list) -> list[tuple[float, float]]:
    return [(point.x, point.y) for point in points]


def generate_synthetic_floorplan_image(annotation: FloorPlanAnnotation, output_path: str | Path) -> Path:
    image = Image.new("RGB", (annotation.image_width, annotation.image_height), "white")
    draw = ImageDraw.Draw(image)

    for room in annotation.rooms:
        draw.polygon(
            _polygon_points(room.polygon.points),
            fill=ROOM_COLORS.get(room.room_type, (240, 240, 240)),
            outline=(30, 30, 30),
        )

    for obj in annotation.objects:
        if obj.bbox is None:
            continue
        draw.rectangle(
            (obj.bbox.x_min, obj.bbox.y_min, obj.bbox.x_max, obj.bbox.y_max),
            fill=OBJECT_COLORS.get(obj.object_type, (80, 80, 80)),
            outline=(20, 20, 20),
        )

    for flow in annotation.flows:
        draw.line(_polygon_points(flow.points), fill=(170, 170, 170), width=3)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a synthetic floor-plan PNG.")
    parser.add_argument("--annotation", required=True, help="Path to synthetic annotation JSON.")
    parser.add_argument("--output", required=True, help="Path to write PNG image.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    annotation = FloorPlanAnnotation.model_validate_json(Path(args.annotation).read_text(encoding="utf-8"))
    output = generate_synthetic_floorplan_image(annotation, args.output)
    print("Synthetic floor-plan image written to " + str(output))
    print("No real Thai FDA data was used.")


if __name__ == "__main__":
    main()
