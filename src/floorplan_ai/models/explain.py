"""Explain synthetic advisory revision-risk predictions."""

from __future__ import annotations

from typing import Any


def top_feature_contributors(model: Any, feature_names: list[str], feature_values: list[float], top_n: int = 5) -> list[dict[str, float | str]]:
    importances = getattr(model, "feature_importances_", [1.0 / len(feature_names)] * len(feature_names))
    rows: list[dict[str, float | str]] = []
    for name, value, importance in zip(feature_names, feature_values, importances):
        rows.append(
            {
                "feature": name,
                "value": float(value),
                "model_importance": float(importance),
                "contribution_score": float(abs(value) * importance),
            }
        )
    return sorted(rows, key=lambda item: float(item["contribution_score"]), reverse=True)[:top_n]
