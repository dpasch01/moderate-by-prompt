# Policy and Component Audit

Agreement with dataset labels does not show that a model follows the supplied definition. The audit labels a sample of test texts directly against each dataset-specific definition and its component questions. The annotations are in `../data/audit/audit_annotations.csv`.

## Sampling

- 50 test texts per dataset, sampled without replacement (seed 20260929).
- Per dataset, 40 texts whose prediction changed with the definition for some model, and 10 whose prediction did not. Each half is balanced on the binary gold label.
- Because the sample oversamples definition-sensitive texts, rates are reweighted by inverse inclusion probability. Raw agreements describe the enriched sample rather than the full test sets.

| Dataset | Changed, hate | Changed, non-hate | Stable, hate | Stable, non-hate |
|---|---:|---:|---:|---:|
| Dynamic | 1,541 / 20 | 1,157 / 20 | 727 / 5 | 695 / 5 |
| MHS | 473 / 20 | 1,255 / 20 | 309 / 5 | 1,166 / 5 |
| HateXplain | 252 / 20 | 971 / 20 | 342 / 5 | 359 / 5 |
| HateCheck | 1,108 / 20 | 678 / 20 | 1,455 / 5 | 487 / 5 |

Cells give population size / sample size per stratum. Each sampled text has weight N/n.

## Annotation

- Annotators saw an anonymous identifier, the text, the supplied definition, and the component questions, in shuffled order. They did not see the dataset name, gold label, or any model output.
- Each annotator gave a policy judgment (meets the definition or not) and an answer to every component question, or marked it uncertain.
- Three human annotators labeled all 200 texts independently.
- The reference for each field (policy judgment or component answer) is the answer given by at least two humans. Uncertain, skipped, or blank answers do not vote. This resolves 184 of 200 policy judgments and all component answers for 180 texts.
- Two fresh-context runs of GPT-6-Astra also labeled all texts. They do not vote in the reference. GPT-6-Astra comes from the same provider as GPT-5.6 Luna, GPT-6 Sol, and Luna Decisions.

## Annotator agreement

- Pairwise agreement between the humans on policy judgments is 97% to 99% (Cohen's κ .95 to .98).
- The two GPT-6-Astra runs agree with the human reference on 178 of 179 and 180 of 180 policy judgments where both are definite.

## Conflicts between the reference and the dataset labels

| Dataset | Conflicts / definite reference | Raw | Reweighted | 95% interval |
|---|---:|---:|---:|---|
| Dynamic | 1 / 46 | 2.2% | 2.0% | 0.0% to 6.5% |
| MHS | 15 / 41 | 36.6% | 22.4% | 12.2% to 35.8% |
| HateXplain | 13 / 47 | 27.7% | 28.1% | 14.7% to 43.2% |
| HateCheck | 2 / 50 | 4.0% | 3.0% | 0.0% to 7.4% |

Intervals use 10,000 cluster resamples per dataset (seed 20260929), poststratified to the original stratum sizes. They are descriptive and approximate under sparse sampling.

## Measures

For each model, we report agreement with the human reference on:

- **Policy:** benchmark-direct predictions.
- **Conflicts:** the subset where the reference conflicts with the dataset label.
- **Components:** texts where all of the model's component answers in decomposed classification match the reference.

## Results

| Model | Policy (%) | Conflicts | Components (%) |
|---|---:|---:|---:|
| Jev | 90 | 23/31 | 69 |
| Laya | 61 | 13/31 | 35 |
| Decider | 65 | 10/31 | 26 |
| SemIf-2B | 51 | 10/31 | 28 |
| SemIf-4B | 70 | 16/31 | 49 |
| Bespoke-Nimble | 68 | 17/31 | 56 |
| Luna Decisions | 78 | 16/31 | 54 |
| CoPE | 80 | 20/31 | 58 |
| BART* | 52 | 8/31 | 39 |
| GPT-5.6 Luna | 90 | 23/31 | 68 |
| GPT-6 Sol | 92 | 21/31 | 80 |

Policy agreement uses 184 texts, conflicts 31, and components 180. \* Policy-free direct baseline.

### Policy agreement by dataset

Correct / definite reference, with the reweighted agreement in parentheses. Benchmark-direct predictions.

| Model | Dynamic | MHS | HateXplain | HateCheck |
|---|---:|---:|---:|---:|
| Jev | 42/46 (92.6%) | 37/41 (94.6%) | 37/47 (77.3%) | 50/50 (100.0%) |
| Laya | 28/46 (61.7%) | 25/41 (70.2%) | 33/47 (68.6%) | 26/50 (56.9%) |
| Decider | 28/46 (60.5%) | 26/41 (77.6%) | 26/47 (56.5%) | 39/50 (87.1%) |
| SemIf-2B | 26/46 (60.4%) | 20/41 (55.3%) | 19/47 (42.4%) | 28/50 (72.0%) |
| SemIf-4B | 30/46 (66.8%) | 27/41 (75.4%) | 34/47 (75.2%) | 37/50 (83.6%) |
| Bespoke-Nimble | 33/46 (78.2%) | 28/41 (79.5%) | 31/47 (60.0%) | 33/50 (77.7%) |
| Luna Decisions | 32/46 (68.7%) | 28/41 (79.5%) | 36/47 (77.2%) | 48/50 (97.0%) |
| CoPE | 34/46 (79.2%) | 34/41 (88.5%) | 33/47 (66.6%) | 46/50 (96.4%) |
| BART* | 23/46 (57.0%) | 19/41 (59.7%) | 24/47 (47.0%) | 30/50 (74.4%) |
| GPT-5.6 Luna | 42/46 (93.1%) | 37/41 (93.0%) | 40/47 (81.4%) | 47/50 (95.5%) |
| GPT-6 Sol | 44/46 (96.5%) | 37/41 (94.6%) | 38/47 (82.6%) | 50/50 (100.0%) |

### Decomposition gains and component correctness

Among audited texts whose verdict decomposition corrected, only 2 of 34 have all component answers correct, so corrected verdicts need not rest on correct component answers.

### Effect of the definition

Supplying the definition moves predictions toward the reference inconsistently, for example by 8 net corrections for Jev on MHS but 2 to 6 net errors for Laya on each of the four datasets.

## Annotation file

`../data/audit/audit_annotations.csv` has one row per audited text with:

- `audit_id`, `item_id` (dataset and original identifier), `dataset`, `policy_id`, `stratum`, `weight`, `dataset_label`
- for each human (`human_01` to `human_03`), the reference (`majority`), and the two GPT-6-Astra runs (`agent_a`, `agent_b`):
  - the policy judgment
  - the component answers as `question=answer` pairs

An empty value means uncertain, skipped, or unresolved. Texts are not redistributed. Use `item_id` to retrieve them from the original datasets.
