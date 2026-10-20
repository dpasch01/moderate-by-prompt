# Can Platforms Moderate by Prompt? Supplementary Repository

This anonymized repository accompanies the submission *Can Platforms Moderate by Prompt? Evaluating Structured Decision Models for Policy-Conditioned Hate-Speech Moderation*. It contains the material that the paper's page limit excludes: complete prompts, model interfaces and settings, additional results, the human annotations of the audit, and the policy-contrast set.

All paths below are relative to the repository root. Section letters refer to the paper's appendix.

## Contents

| Path | Contents | Paper reference |
|---|---|---|
| `prompts/definitions.md` | Dataset-specific definitions and the generic definition | Appendix A |
| `prompts/decomposition_questions.md` | Component questions with full answer descriptions, and the fixed rules | Appendix B |
| `prompts/instructions.md` | Instruction templates for binary, three-class, attribute, and decomposition tasks | Appendix C |
| `prompts/model_interfaces.md` | Request formats for every model, and the adaptation of CoPE and BART to decomposition | Appendix C |
| `settings/models.md`, `settings/models.csv` | Pinned checkpoints, precision, input limits, and decision rules | Appendix C |
| `settings/inference_settings.md` | Truncation, tie-breaking, commercial API settings, refusals, hardware, and supervised training settings | Section 3, Appendix C |
| `results/benchmark_direct.md`, `results/benchmark_direct.csv` | Benchmark-direct binary and three-class macro-F1 for all models | Table 2, Appendix F |
| `results/luna_decisions_coverage.md` | Luna Decisions requests, refusals, and paired valid texts per condition | Table 2, Appendix C |
| `results/supervised_transfer.csv` | Cross-dataset macro-F1 of the supervised classifiers | Appendix D |
| `results/attributes.md` | Conduct, group, and direction macro-F1 | Appendix D |
| `results/class_description_ablation.md` | Ablation separating the definition from the class descriptions | Section 4.2 |
| `results/definition_flips.md` | Predictions changed, corrected, and broken by the definition | Section 4.2, Appendix E |
| `results/three_class.md` | Per-class F1 on HateXplain's three-class task | Appendix F |
| `results/efficiency.md`, `results/efficiency.csv` | Median and 95th-percentile latency, throughput, and cost for all models | Appendix H, Figure 3 |
| `results/cascades.md` | Cascade protocol, results, estimated and live latency, and the cascade curves | Appendix I |
| `results/audit_protocol.md` | Protocol and results of the policy and component audit | Section 4.2, Table 3, Appendix J |
| `data/audit/audit_annotations.csv` | Human and GPT-6-Astra annotations of the 200 audited texts (identifiers only) | Appendix J |
| `data/policy_contrast/` | Policy-contrast policies, 240 texts, expected labels, annotations, validation, and model results | Sections 3 and 4.2, Appendix K |
| `results/decider_exposure.md` | Decider training-exposure replay results | Section 5 |
| `results/generic_definition.md` | Effect of the generic definition (early experiments) | Not in paper |
| `results/selective_routing.md` | Exploratory selective-routing analysis (earlier cohorts) | Not in paper |
| `figures/` | Cascade curves and the supervised-transfer heatmap | Appendix D, I |
| `code/` | Evaluation and analysis code (released upon acceptance) | Section 3 |
| `CHANGELOG.md` | Changes since the first version of this repository | |

## Datasets

The study uses four public datasets under their terms of use: Dynamic (Dynamically Generated Hate Speech Dataset), Measuring Hate Speech (MHS), HateXplain, and HateCheck. The datasets are not redistributed here. `code/README.md` lists their sources, and the code released upon acceptance reproduces the test partitions and linked groups.

## Notes

- Texts in the datasets contain hateful and offensive language. This repository reproduces definitions, instructions, and prompts, but no dataset texts. Audit annotations refer to texts by their dataset identifiers.
- **Content warning:** `data/policy_contrast/texts.csv` contains constructed hateful statements filled into HateCheck templates. They exist only to test whether models follow a change in policy.
- Hosted model identifiers do not guarantee unchanged weights over time. Exact reproduction of hosted results may therefore not be possible.
