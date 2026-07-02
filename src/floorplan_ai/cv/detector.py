"""Simple color-based detection for synthetic floor-plan images."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOM_COLORS: dict[str, tuple[int, int, int]] = {
    "production_area": (230, 242, 255),
    "raw_material_storage": (228, 247, 232),
    "finished_product_storage": (255, 242, 217),
    "packaging_area": (244, 232, 255),
    "washing_area": (218, 246, 245),
    "toilet": (255, 224, 224),
    "waste_area": (230, 230, 230),
    "corridor": (245, 245, 245),
    "unknown": (255, 250, 205),
    "unlabeled_room": (255, 250, 205),
}

OBJECT_COLORS: dict[str, tuple[int, int, int]] = {
    "door": (88, 88, 88),
    "window": (62, 142, 208),
    "sink": (45, 162, 184),
    "handwashing_point": (34, 139, 94),
    "drain": (90, 90, 160),
    "equipment": (176, 112, 58),
}


@dataclass(frozen=True)
class Detection:
    detection_id: str
    category: str
    label: str
    bbox: tuple[int, int, int, int]
    confidence: float
    source: str = "synthetic_color_detector"


def _component_boxes(image: Image.Image, target_color: tuple[int, int, int], min_pixels: int) -> list[tuple[int, int, int, int]]:
    pixels = image.load()
    width, height = image.size
    visited: set[tuple[int, int]] = set()
    boxes: list[tuple[int, int, int, int]] = []

    for y in range(height):
        for x in range(width):
            if (x, y) in visited or pixels[x, y] != target_color:
                continue
            queue: deque[tuple[int, int]] = deque([(x, y)])
            visited.add((x, y))
            xs: list[int] = []
            ys: list[int] = []
            while queue:
                cx, cy = queue.popleft()
                xs.append(cx)
                ys.append(cy)
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height or (nx, ny) in visited:
                        continue
                    if pixels[nx, ny] == target_color:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            if len(xs) >= min_pixels:
                boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    return boxes


def detect_synthetic_floorplan(image_path: str | Path, min_room_pixels: int = 500) -> list[Detection]:
    """Detect color-coded synthetic rooms and objects in a generated PNG."""

    image = Image.open(image_path).convert("RGB")
    detections: list[Detection] = []

    for label, color in ROOM_COLORS.items():
        boxes = _component_boxes(image, color, min_room_pixels)
        for index, box in enumerate(boxes, start=1):
            detections.append(
                Detection(
                    detection_id=f"det-room-{label}-{index}",
                    category="room",
                    label=label,
                    bbox=box,
                    confidence=0.98,
                )
            )

    for label, color in OBJECT_COLORS.items():
        boxes = _component_boxes(image, color, min_pixels=20)
        for index, box in enumerate(boxes, start=1):
            detections.append(
                Detection(
                    detection_id=f"det-object-{label}-{index}",
                    category="object",
                    label=label,
                    bbox=box,
                    confidence=0.96,
                )
            )

    return sorted(detections, key=lambda item: (item.category, item.label, item.bbox))
