# Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Prototype interpreted as automatic approval or rejection | Regulatory misuse | Advisory-only language in README, report, CLI, app, and findings |
| Real Thai FDA or applicant data committed | Confidentiality breach | Synthetic-only data policy and prohibited-data list |
| Poor annotation quality | Incorrect findings | Human review required and annotation guide provided |
| Simplified rules miss context | False reassurance or false concern | Explainable findings and officer interpretation required |
| Heatmap overstates precision | Misleading visual interpretation | Use heatmap as review aid only, paired with explanations |
| Future real-world pilot lacks governance | Privacy and compliance risk | Require formal data governance before non-synthetic data |
| Synthetic CV demo mistaken for real drawing parser | Incorrect expectations or misuse | Document Phase 3 as color-coded synthetic detection only |
| Synthetic ML metrics mistaken for validation | False confidence | Label Phase 4 metrics as synthetic holdout metrics only |
| Workflow simulation mistaken for operational deployment | Premature adoption | Keep Phase 5 reports advisory and require officer responsibility |

## Phase 2 Deferred

Phase 2 is deferred. This repository currently uses synthetic data only. Real Thai FDA de-identified data and expert annotation are required before validation or operational use.

## Current Synthetic Prototype Status

The project is a research prototype with synthetic sample data, deterministic rules, synthetic CV extraction, synthetic ML revision-risk prediction, and synthetic workflow simulation. It is suitable for demonstration, testing, and discussion of workflow design, not production regulatory use.
