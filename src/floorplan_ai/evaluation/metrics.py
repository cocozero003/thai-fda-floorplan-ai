"""Evaluation metrics for synthetic screening experiments."""

from __future__ import annotations


def precision(y_true: list[int], y_pred: list[int]) -> float:
    values = confusion_matrix(y_true, y_pred)
    denominator = values["tp"] + values["fp"]
    return float(values["tp"] / denominator) if denominator else 0.0


def recall(y_true: list[int], y_pred: list[int]) -> float:
    return sensitivity(y_true, y_pred)


def f1_score(y_true: list[int], y_pred: list[int]) -> float:
    score_precision = precision(y_true, y_pred)
    score_recall = recall(y_true, y_pred)
    denominator = score_precision + score_recall
    return float(2 * score_precision * score_recall / denominator) if denominator else 0.0


def confusion_matrix(y_true: list[int], y_pred: list[int]) -> dict[str, int]:
    _validate_same_length(y_true, y_pred)
    values = {"tn": 0, "fp": 0, "fn": 0, "tp": 0}
    for actual, predicted in zip(y_true, y_pred):
        if actual == 1 and predicted == 1:
            values["tp"] += 1
        elif actual == 0 and predicted == 0:
            values["tn"] += 1
        elif actual == 0 and predicted == 1:
            values["fp"] += 1
        elif actual == 1 and predicted == 0:
            values["fn"] += 1
        else:
            raise ValueError("binary metrics expect labels 0 or 1")
    return values


def sensitivity(y_true: list[int], y_pred: list[int]) -> float:
    values = confusion_matrix(y_true, y_pred)
    denominator = values["tp"] + values["fn"]
    return float(values["tp"] / denominator) if denominator else 0.0


def specificity(y_true: list[int], y_pred: list[int]) -> float:
    values = confusion_matrix(y_true, y_pred)
    denominator = values["tn"] + values["fp"]
    return float(values["tn"] / denominator) if denominator else 0.0


def percent_agreement(rater_a: list[int], rater_b: list[int]) -> float:
    _validate_same_length(rater_a, rater_b)
    if not rater_a:
        return 0.0
    agreements = sum(1 for left, right in zip(rater_a, rater_b) if left == right)
    return float(agreements / len(rater_a))


def cohen_kappa(rater_a: list[int], rater_b: list[int]) -> float:
    _validate_same_length(rater_a, rater_b)
    if not rater_a:
        return 0.0

    labels = sorted(set(rater_a) | set(rater_b))
    observed = percent_agreement(rater_a, rater_b)
    expected = 0.0
    total = len(rater_a)
    for label in labels:
        left_probability = sum(1 for value in rater_a if value == label) / total
        right_probability = sum(1 for value in rater_b if value == label) / total
        expected += left_probability * right_probability

    denominator = 1.0 - expected
    return float((observed - expected) / denominator) if denominator else 0.0


def _validate_same_length(left: list[int], right: list[int]) -> None:
    if len(left) != len(right):
        raise ValueError("input lists must have the same length")
