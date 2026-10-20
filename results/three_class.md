# Three-Class Results

Per-class F1 on HateXplain's three-class task (1,924 posts: 594 hate, 548 offensive, 782 normal), and the share of offensive posts labeled hate or normal. Summarized in Appendix F of the paper.

| Model | F1 hate | F1 offensive | F1 normal | Offensive labeled hate | Offensive labeled normal |
|---|---:|---:|---:|---:|---:|
| Laya | .707 | .346 | .693 | 41% | 34% |
| GPT-6 Sol | .710 | .464 | .674 | 37% | 17% |
| Luna Decisions | .698 | .468 | .677 | 26% | 23% |
| TF-IDF+LR | .736 | .471 | .717 | - | - |
| DistilBERT | .733 | .450 | .728 | - | - |

All models score lowest on the offensive class. The out-of-the-box models label more offensive posts as hate than as normal, so the principal confusion lies between offensive and hateful language. The supervised classifiers are trained on a 5,000-post subset of the training partition. Macro-F1 for every model is in `benchmark_direct.md`.
