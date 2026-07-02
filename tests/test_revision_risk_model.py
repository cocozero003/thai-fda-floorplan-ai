from pathlib import Path

from floorplan_ai.models.dataset import FEATURE_NAMES, generate_synthetic_training_rows, write_synthetic_training_csv
from floorplan_ai.models.predict_revision_risk import predict_revision_risk
from floorplan_ai.models.train_revision_risk import train_revision_risk_model


def test_train_and_predict_revision_risk_model(tmp_path: Path) -> None:
    training_csv = write_synthetic_training_csv(generate_synthetic_training_rows(90, seed=4), tmp_path / "training.csv")
    model_path = tmp_path / "model.pkl"

    metrics = train_revision_risk_model(training_csv, model_path)
    prediction = predict_revision_risk(model_path, {name: 1.0 for name in FEATURE_NAMES})

    assert model_path.exists()
    assert metrics["synthetic_data_only"] is True
    assert prediction["advisory_only"] is True
    assert prediction["revision_risk_class"] in {"low", "medium", "high"}
    assert set(prediction["class_probabilities"]).issubset({"low", "medium", "high"})
    assert prediction["top_feature_contributors"]
