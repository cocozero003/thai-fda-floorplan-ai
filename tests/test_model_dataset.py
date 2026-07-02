from pathlib import Path

from floorplan_ai.models.dataset import FEATURE_NAMES, generate_synthetic_training_rows, load_training_csv, write_synthetic_training_csv


def test_generate_synthetic_training_rows_have_expected_features() -> None:
    rows = generate_synthetic_training_rows(count=20, seed=7)

    assert len(rows) == 20
    assert set(FEATURE_NAMES).issubset(rows[0].keys())
    assert {row["revision_risk_class"] for row in rows}.issubset({"low", "medium", "high"})


def test_write_and_load_training_csv(tmp_path: Path) -> None:
    output = write_synthetic_training_csv(generate_synthetic_training_rows(count=12), tmp_path / "training.csv")
    features, labels, rows = load_training_csv(output)

    assert len(features) == 12
    assert len(labels) == 12
    assert rows[0]["case_id"].startswith("synthetic-training-")
