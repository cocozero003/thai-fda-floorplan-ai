"""Predict advisory revision-risk classes with synthetic models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from floorplan_ai.models.dataset import FEATURE_NAMES, SYNTHETIC_DATA_WARNING, feature_vector
from floorplan_ai.models.explain import top_feature_contributors
from floorplan_ai.models.train_revision_risk import load_model_package


def predict_revision_risk(model_path: str | Path, feature_map: dict[str, float]) -> dict[str, Any]:
    package = load_model_package(model_path)
    model = package["model"]
    values = feature_vector(feature_map)
    probabilities = model.predict_proba([values])[0]
    classes = list(model.classes_)
    predicted_class = classes[int(probabilities.argmax())]
    return {
        "advisory_only": True,
        "human_review_required": True,
        "synthetic_data_only": True,
        "warning": SYNTHETIC_DATA_WARNING,
        "revision_risk_class": predicted_class,
        "class_probabilities": {label: float(probability) for label, probability in zip(classes, probabilities)},
        "top_feature_contributors": top_feature_contributors(model, FEATURE_NAMES, values),
        "features": {name: float(feature_map.get(name, 0.0)) for name in FEATURE_NAMES},
    }
