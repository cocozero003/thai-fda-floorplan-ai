"""Preprocessing utilities for synthetic floor-plan images."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter, ImageOps


def preprocess_image(image_path: str | Path, threshold: int = 245) -> dict[str, Any]:
    """Load a synthetic floor-plan image and return simple derived images."""

    image = Image.open(image_path).convert("RGB")
    grayscale = ImageOps.grayscale(image)
    denoised = grayscale.filter(ImageFilter.MedianFilter(size=3))
    binary = denoised.point(lambda pixel: 255 if pixel >= threshold else 0, mode="1")
    return {
        "image": image,
        "grayscale": grayscale,
        "binary": binary.convert("L"),
        "width": image.width,
        "height": image.height,
        "synthetic_data_only": True,
    }
