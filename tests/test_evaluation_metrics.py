import pytest

from floorplan_ai.evaluation.metrics import (
    cohen_kappa,
    confusion_matrix,
    f1_score,
    percent_agreement,
    precision,
    recall,
    sensitivity,
    specificity,
)


def test_binary_classification_metrics() -> None:
    y_true = [1, 0, 1, 1, 0, 0]
    y_pred = [1, 0, 1, 0, 0, 1]

    assert precision(y_true, y_pred) == pytest.approx(2 / 3)
    assert recall(y_true, y_pred) == pytest.approx(2 / 3)
    assert f1_score(y_true, y_pred) == pytest.approx(2 / 3)
    assert confusion_matrix(y_true, y_pred) == {"tn": 2, "fp": 1, "fn": 1, "tp": 2}
    assert sensitivity(y_true, y_pred) == pytest.approx(2 / 3)
    assert specificity(y_true, y_pred) == pytest.approx(2 / 3)


def test_agreement_metrics() -> None:
    rater_a = [1, 0, 1, 1]
    rater_b = [1, 0, 0, 1]

    assert percent_agreement(rater_a, rater_b) == pytest.approx(0.75)
    assert cohen_kappa(rater_a, rater_b) == pytest.approx(0.5)


def test_percent_agreement_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        percent_agreement([1], [1, 0])
