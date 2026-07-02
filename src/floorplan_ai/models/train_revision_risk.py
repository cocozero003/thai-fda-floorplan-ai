"""Train synthetic advisory revision-risk models."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from floorplan_ai.models.dataset import FEATURE_NAMES, SYNTHETIC_DATA_WARNING, load_training_csv


def train_revision_risk_model(
    training_csv: str | Path,
    model_output: str | Path,
    random_state: int = 42,
) -> dict[str, Any]:
    features, labels, rows = load_training_csv(training_csv)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.25,
        random_state=random_state,
        stratify=labels,
    )
    model = RandomForestClassifier(n_estimators=120, random_state=random_state, max_depth=6)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    evaluation = {
        "synthetic_data_only": True,
        "warning": SYNTHETIC_DATA_WARNING,
        "training_rows": len(rows),
        "holdout_rows": len(y_test),
        "holdout_accuracy_on_synthetic_data": accuracy_score(y_test, predictions),
        "feature_names": FEATURE_NAMES,
        "classes": list(model.classes_),
    }
    package = {
        "model": model,
        "feature_names": FEATURE_NAMES,
        "evaluation": evaluation,
        "warning": SYNTHETIC_DATA_WARNING,
    }
    output = Path(model_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as file:
        pickle.dump(package, file)
    return evaluation


def load_model_package(model_path: str | Path) -> dict[str, Any]:
    with Path(model_path).open("rb") as file:
        return pickle.load(file)
