# Can Platforms Moderate by Prompt? Supplementary Repository

This anonymized repository accompanies the submission *Can Platforms Moderate by Prompt? Evaluating Structured Decision Models for Policy-Conditioned Hate-Speech Moderation*. It contains the material that the paper's page limit excludes: complete prompts, model interfaces and settings, and additional results.

All paths below are relative to the repository root. Section letters refer to the paper's appendix.

## Contents

| Path | Contents | Paper reference |
|---|---|---|
| `prompts/definitions.md` | Dataset-specific definitions and the generic definition | Appendix A |
| `prompts/decomposition_questions.md` | Component questions with full answer descriptions, and the fixed rules | Appendix B |
| `prompts/instructions.md` | Instruction templates for binary, three-class, attribute, and decomposition tasks | Appendix C |
| `prompts/model_interfaces.md` | Request formats for every model, and the adaptation of CoPE and BART to decomposition | Appendix C |
| `settings/models.md`, `settings/models.csv` | Pinned checkpoints, precision, input limits, and decision rules | Appendix C |
| `settings/inference_settings.md` | Truncation, tie-breaking, commercial API settings, and refusals | Appendix C |
| `results/supervised_transfer.csv` | Cross-dataset macro-F1 of the supervised classifiers | Appendix D |
| `results/generic_definition.md` | Effect of the generic definition (early experiments) | Not in paper |
| `results/efficiency.md`, `results/efficiency.csv` | Median and 95th-percentile latency, throughput, and cost for all models | Appendix H, Figure 4 |
| `results/cascades.md` | Cascade protocol and results, with the cascade curves | Appendix I |
| `results/selective_routing.md` | Exploratory selective-routing analysis (earlier cohorts) | Not in paper |
| `results/audit_protocol.md` | Sampling, annotation, and reweighting protocol of the policy and component audit | Appendix J |
| `results/decider_exposure.md` | Full Decider training-exposure replay results | Appendix K |
| `figures/` | Cascade curves and the supervised-transfer heatmap | Appendix D, I |
| `code/` | Evaluation and analysis code (released upon acceptance) | Section 3 |

## Datasets

The study uses four public datasets under their terms of use: Dynamic (Dynamically Generated Hate Speech Dataset), Measuring Hate Speech (MHS), HateXplain, and HateCheck. The datasets are not redistributed here. `code/README.md` lists their sources, and the code released upon acceptance reproduces the test partitions and linked groups.

## Notes

- Texts in the datasets contain hateful and offensive language. This repository reproduces only definitions, instructions, and prompts, not dataset texts.
- Hosted model identifiers do not guarantee unchanged weights over time. Exact reproduction of hosted results may therefore not be possible.
- The human annotation of the audit is in progress at submission time. Figures marked as pending in the paper will be updated here.
