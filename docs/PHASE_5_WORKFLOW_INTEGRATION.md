# Phase 5 Workflow Integration Prototype

Phase 5 is a synthetic Thai FDA officer workflow simulation.

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

## What It Does

- Creates synthetic screening cases.
- Runs advisory rule-based findings.
- Optionally includes synthetic ML revision-risk prediction.
- Supports officer comments and override fields.
- Exports officer-facing Markdown and JSON reports.
- Writes an audit log.

## Human Oversight

The workflow does not approve or reject applications. Officer comments and overrides are recorded as review fields, not automated decisions. Human Thai FDA officers remain responsible for all regulatory decisions.

## Demo

```bash
python scripts/run_workflow_demo.py \
  --annotation data/sample_synthetic/annotation_simple_factory.json \
  --rules configs/rules_gmp_thai_fda.yaml \
  --markdown-output outputs/synthetic_officer_report.md \
  --json-output outputs/synthetic_officer_report.json \
  --audit-output outputs/synthetic_audit_log.json \
  --model outputs/synthetic_revision_risk_model.pkl
```
