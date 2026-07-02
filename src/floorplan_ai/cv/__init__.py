"""Synthetic computer vision helpers for floor-plan demonstrations."""

from floorplan_ai.cv.annotation_converter import detections_to_annotation
from floorplan_ai.cv.detector import Detection, detect_synthetic_floorplan
from floorplan_ai.cv.preprocess import preprocess_image

__all__ = [
    "Detection",
    "detect_synthetic_floorplan",
    "detections_to_annotation",
    "preprocess_image",
]
