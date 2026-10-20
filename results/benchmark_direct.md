# Benchmark-Direct Classification

Benchmark-direct classification gives the model the dataset-specific definition and class descriptions and asks it to select the label. It is the main condition of the paper (Table 2, column "Bench."). Matched direct (A) and decomposed (B) classification also receive the decomposition rule and component glossary. Their results are in Table 2 of the paper.

Binary macro-F1 on the full test sets. A machine-readable version with valid Ns is in `benchmark_direct.csv`.

| Model | Dynamic | MHS | HateXplain | HateCheck |
|---|---:|---:|---:|---:|
| Jev | .832 | .689 | .691 | .970 |
| Laya | .639 | .692 | .753 | .709 |
| Decider | .623 | .794 | .610 | .781 |
| SemIf-2B | .584 | .442 | .548 | .656 |
| SemIf-4B | .652 | .725 | .692 | .786 |
| Bespoke-Nimble | .772 | .616 | .459 | .785 |
| Luna Decisions | .716 | .658 | .776 | .909 |
| CoPE | .810 | .653 | .587 | .913 |
| BART* | .614 | .587 | .516 | .729 |
| GPT-5.6 Luna | .873 | .695 | .670 | .974 |
| GPT-6 Sol | .891 | .698 | .784 | .973 |

- Binary HateXplain uses the Davidson proxy definition, mapping hatespeech to hate and the other two classes to non-hate.
- \* BART's benchmark-direct result is its definition-free formulation.
- Luna Decisions has 4,111 valid outputs on Dynamic and 3,719 on HateCheck. Refusals are excluded (`luna_decisions_coverage.md`).
- Labeling every MHS comment non-hate gives .430.

## HateXplain three-class

Macro-F1 on all 1,924 test posts (594 hate, 548 offensive, 782 normal).

| Model | Macro-F1 |
|---|---:|
| Jev | .544 |
| Laya | .582 |
| Decider | .511 |
| SemIf-2B | .277 |
| SemIf-4B | .401 |
| Bespoke-Nimble | .375 |
| Luna Decisions | .615 |
| CoPE | .253 |
| BART* | .271 |
| GPT-5.6 Luna | .519 |
| GPT-6 Sol | .616 |
| TF-IDF+LR | .642 |
| DistilBERT | .637 |

Per-class scores for selected models are in `three_class.md`.
