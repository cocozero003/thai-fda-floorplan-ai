# Phase 4 Synthetic Revision-Risk Model

Phase 4 is a synthetic machine learning demonstration for advisory revision-risk prediction.

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

## What It Does

- Generates synthetic training rows.
- Trains a scikit-learn classifier.
- Predicts an advisory revision-risk class.
- Outputs class probabilities.
- Outputs top feature contributors.

## Important Limits

- The model is trained only on synthetic rows.
- Reported metrics are synthetic holdout metrics, not real-world performance.
- The prediction is advisory decision support only.
- Human Thai FDA officers remain responsible for all regulatory decisions.

## Demo

```bash
python scripts/generate_synthetic_training_data.py \
  --output outputs/synthetic_revision_training.csv \
  --count 160

python scripts/train_revision_risk_model.py \
  --training-data outputs/synthetic_revision_training.csv \
  --model-output outputs/synthetic_revision_risk_model.pkl \
  --metrics-output outputs/synthetic_revision_risk_metrics.json

python scripts/predict_revision_risk.py \
  --model outputs/synthetic_revision_risk_model.pkl \
  --screening-report outputs/demo_report.json \
  --output outputs/synthetic_revision_risk_prediction.json
```
