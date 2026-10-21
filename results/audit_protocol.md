# Policy and Component Audit

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

## Final annotation setup

The final reference combines one expert hate-speech researcher with two LLM judges: Opus (`anthropic/claude-opus-5.5`) and Gemini (`google/gemini-4-argon`). Each supplied a policy judgment and each component answer. The expert and judges were shown the policy and questions, without dataset labels or other model predictions. This is a mixed expert–LLM reference, not human-only ground truth.

For each field, at least two matching definite votes establish the reference. Uncertain, missing, blank and skipped answers do not vote; fewer than two agreeing votes is unresolved. The policy verdict is voted directly, not derived from the component majority. This resolves **187/200 policy judgments** and all components for **180/200 texts**.

An earlier annotation round was replaced following receipt of the final expert annotations and adoption of the expert–Opus–Gemini reference.

Judge decoding: maximum 1,024 output tokens, strict JSON schema, one outstanding request per run; temperature, top-p, reasoning and sampling seed were not explicitly set. Hosted model aliases do not identify immutable weight revisions. All model-versus-reference analyses below reuse cached predictions.

## Expert–judge agreement

Raw agreement and Cohen kappa on mutually definite answers; uncertain/missing answers excluded. These are comparisons against the individual expert, not against the majority reference.

| Judge | Policy agreement | Cohen kappa | Component-answer agreement |
|---|---:|---:|---:|
| Opus | 174/182 (95.6%) | 0.912 | 371/410 (90.5%) |
| Gemini | 170/180 (94.4%) | 0.888 | 364/423 (86.1%) |

Pooling heterogeneous component questions does not define one meaningful component kappa. With uncertainty treated as a category, policy agreement/kappa are Opus 89.5%/.810 and Gemini 87.0%/.765 (N=200).

## Reference–dataset conflicts by dataset

| Dataset | Conflicts / resolved | Raw % [95% Wilson] | Reweighted % [95% cluster bootstrap] |
|---|---:|---|---|
| Dynamic | 2/49 | 4.1 [1.1, 13.7] | 3.3 [0.0, 8.6] |
| MHS | 17/44 | 38.6 [25.7, 53.4] | 20.7 [12.3, 31.5] |
| HateXplain | 9/46 | 19.6 [10.7, 33.2] | 16.6 [6.5, 27.8] |
| HateCheck | 1/48 | 2.1 [0.4, 10.9] | 1.5 [0.0, 5.0] |

Raw intervals are descriptive Wilson intervals. Reweighted intervals use the existing 10,000-draw cluster bootstrap, seed 20260929, retaining the original dataset order and poststratifying each draw to the sampling stratum populations. Draws missing a stratum or a resolved reference denominator are omitted; intervals are approximate for this sparse enriched sample.

Dynamic: 9918/10000 weighted-bootstrap draws retained; 50 sampled clusters.
MHS: 9895/10000 weighted-bootstrap draws retained; 50 sampled clusters.
HateXplain: 9886/10000 weighted-bootstrap draws retained; 50 sampled clusters.
HateCheck: 9896/10000 weighted-bootstrap draws retained; 50 sampled clusters.

## Model results

Agree uses benchmark-direct predictions on all 187 resolved policy judgments; every model has a valid prediction on these texts. Conflicts counts agreement with the reference on the 29 reference?dataset conflicts. Comp. requires every decomposed-B component to match, among the 180 texts whose component references all resolve. BART benchmark direct is the policy-free NLI baseline. These are raw enriched-sample percentages, not population accuracy.

| Model | Agree % (k/187) | Conflicts k/29 [95% Wilson %] | Comp. % (k/180) |
|---|---:|---|---:|
| Jev | 88.8 (166/187) | 21/29 [54.3, 85.3] | 71.7 (129/180) |
| Laya | 61.5 (115/187) | 13/29 [28.4, 62.5] | 38.9 (70/180) |
| Decider | 64.2 (120/187) | 9/29 [17.3, 49.2] | 31.1 (56/180) |
| SemIf-2B | 48.1 (90/187) | 8/29 [14.7, 45.7] | 26.7 (48/180) |
| SemIf-4B | 70.6 (132/187) | 16/29 [37.5, 71.6] | 52.2 (94/180) |
| Nimble NF4 | 65.2 (122/187) | 14/29 [31.4, 65.6] | 50.6 (91/180) |
| Luna Decisions | 80.7 (151/187) | 19/29 [47.3, 80.1] | 57.2 (103/180) |
| CoPE NF4 | 78.1 (146/187) | 18/29 [44.0, 77.3] | 57.2 (103/180) |
| BART | 53.5 (100/187) | 9/29 [17.3, 49.2] | 35.6 (64/180) |
| GPT-5.6 Luna | 89.3 (167/187) | 22/29 [57.9, 87.8] | 62.8 (113/180) |
| GPT-6 Sol | 93.0 (174/187) | 21/29 [54.3, 85.3] | 76.1 (137/180) |

Jev 21/29, Luna 22/29, Sol 21/29 on conflicts. Agree for Sol/Jev/Luna: 88.8?93.0%; other decision models (Laya, Decider, SemIf-2B, SemIf-4B, Nimble, Luna Decisions): 48.1?80.7%. Component agreement: 26.7% (SemIf-2B) to 76.1% (Sol).

## Decomposition corrected pairs

Matched A wrong to matched B correct relative to the new policy reference, paired-valid only. These are model?text pairs, not distinct texts.

| Model | Corrected pairs | All components correct | Component reference unresolved |
|---|---:|---:|---:|
| Jev | 2 | 2 | 0 |
| Laya | 19 | 6 | 1 |
| Decider | 21 | 7 | 1 |
| SemIf-2B | 43 | 13 | 2 |
| SemIf-4B | 19 | 11 | 1 |
| Nimble NF4 | 14 | 6 | 2 |
| Luna Decisions | 8 | 4 | 0 |
| CoPE NF4 | 3 | 2 | 0 |
| BART | 1 | 0 | 0 |
| GPT-5.6 Luna | 7 | 6 | 0 |
| GPT-6 Sol | 3 | 3 | 0 |

Total: 140 corrected model?text pairs, 60 with all components correct, 7 with unresolved component references. Therefore 60/133 among component-resolved corrected pairs; 60/140 of all corrected pairs are established all-component-correct. Exact corrected-pair IDs are listed below.

## Net corrections from the definition

Historical no-definition -> dataset-specific benchmark direct. Cells show corrected ? introduced = net (paired N). No ablation C1 substitution.

| Model | Dynamic | MHS | HateXplain | HateCheck |
|---|---|---|---|---|
| Jev | 2 ? 2 = +0 (N=49) | 10 ? 1 = +9 (N=44) | 3 ? 1 = +2 (N=46) | 2 ? 0 = +2 (N=48) |
| Laya | 2 ? 5 = -3 (N=49) | 1 ? 7 = -6 (N=44) | 0 ? 4 = -4 (N=46) | 1 ? 7 = -6 (N=48) |
| Decider | 6 ? 2 = +4 (N=49) | 0 ? 4 = -4 (N=44) | 3 ? 8 = -5 (N=46) | 11 ? 5 = +6 (N=48) |
| SemIf-2B | 4 ? 5 = -1 (N=49) | 3 ? 0 = +3 (N=44) | 1 ? 10 = -9 (N=46) | 2 ? 2 = +0 (N=48) |
| SemIf-4B | 6 ? 7 = -1 (N=49) | 8 ? 3 = +5 (N=44) | 7 ? 5 = +2 (N=46) | 4 ? 3 = +1 (N=48) |
| Nimble NF4 | 8 ? 6 = +2 (N=49) | 11 ? 2 = +9 (N=44) | 0 ? 1 = -1 (N=46) | 8 ? 11 = -3 (N=48) |
| Luna Decisions | 3 ? 6 = -3 (N=49) | 0 ? 3 = -3 (N=44) | 3 ? 5 = -2 (N=46) | 2 ? 0 = +2 (N=48) |
| CoPE NF4 | 2 ? 6 = -4 (N=49) | 6 ? 1 = +5 (N=44) | 2 ? 1 = +1 (N=46) | 0 ? 3 = -3 (N=48) |
| BART | Unavailable | Unavailable | Unavailable | Unavailable |
| GPT-5.6 Luna | 0 ? 2 = -2 (N=49) | 3 ? 2 = +1 (N=44) | 3 ? 2 = +1 (N=46) | 0 ? 2 = -2 (N=48) |
| GPT-6 Sol | 0 ? 0 = +0 (N=21) PARTIAL | Unavailable | Unavailable | Unavailable |

Sol is unfinished: its historical no-definition run supplies only 21 paired resolved audit items in Dynamic; other datasets are unavailable. BART has no distinct compatible no-definition intervention.

## MHS neither-selection subset

The 1,477 comments are in neither the replayed training selection nor its 1,500-ID evaluation partition. This is exposure under a public recipe, not proven exposure/nonexposure of released weights. Dataset-label fixed-binary macro-F1; benchmark direct. Same full-MHS cluster resampling as the existing overlap protocol before selecting the subgroup, 10,000 draws, seed 20260929; shared draws for paired differences. Unadjusted descriptive percentile 95% intervals.

| Contrast | N | Difference (pp) | 95% paired interval (pp) |
|---|---:|---:|---|
| Decider-minus-jev | 1477 | +8.892 | [+6.242, +11.551] |
| Decider-minus-sol | 1477 | +8.739 | [+5.704, +11.736] |

Subset macro-F1: decider=0.779816269, jev=0.690894749, sol=0.692429145.

## Threshold-control intervals

All 48 A*?A and A*?B intervals were rerun with 10,000 paired cluster bootstrap draws, seed 20260929, fixed-label binary macro-F1. Primary and exploratory families remain separate at 24 contrasts each. Bonferroni quantiles: 0.05/(2?24) and 1?0.05/(2?24). Every rerun reproduces the saved point estimate, paired N, cluster count, adjusted and unadjusted interval to numerical precision. The full 24-row table is below; this is full-test dataset-label evaluation, not the audit sample.

| Model | Dataset | Family | A* - A [adjusted 95%] (N) | A* - B [adjusted 95%] (N) |
|---|---|---|---|---|
| Laya | Dynamic | primary | -0.44 [-1.00, +0.12] (4120) | +11.64 [+9.40, +13.91] (4120) |
| Laya | MHS | primary | +0.07 [-2.61, +2.95] (3203) | -3.78 [-6.60, -0.95] (3203) |
| Laya | HateXplain | primary | +5.91 [+2.85, +8.93] (1924) | +1.27 [-1.43, +4.02] (1924) |
| SemIf-4B | Dynamic | primary | +4.31 [+2.56, +6.10] (4120) | +6.31 [+4.29, +8.41] (4120) |
| SemIf-4B | MHS | primary | -0.89 [-3.32, +1.38] (3203) | +2.67 [+0.49, +4.91] (3203) |
| SemIf-4B | HateXplain | primary | +4.96 [+1.69, +8.09] (1924) | +4.69 [+1.70, +7.67] (1924) |
| Jev | Dynamic | primary | +2.59 [+1.50, +3.76] (4120) | +0.98 [-0.05, +2.05] (4120) |
| Jev | MHS | primary | +0.12 [-1.95, +2.10] (3203) | +0.92 [-1.06, +2.91] (3203) |
| Jev | HateXplain | primary | +3.45 [+0.39, +6.68] (1924) | +4.25 [+0.95, +7.56] (1924) |
| Luna Decisions | Dynamic | primary | +11.78 [+9.84, +13.65] (4098) | +1.21 [-0.36, +2.82] (4098) |
| Luna Decisions | MHS | primary | +1.57 [+0.29, +3.06] (3203) | +4.26 [+2.05, +6.47] (3203) |
| Luna Decisions | HateXplain | primary | -0.45 [-2.06, +1.06] (1924) | +2.55 [+0.41, +4.68] (1924) |
| Decider | Dynamic | secondary | +10.34 [+8.08, +12.82] (4120) | +13.50 [+10.90, +16.04] (4120) |
| Decider | MHS | secondary | +0.48 [-1.33, +2.19] (3203) | +9.75 [+6.82, +12.75] (3203) |
| Decider | HateXplain | secondary | +3.92 [+0.30, +7.62] (1924) | +0.86 [-2.50, +4.27] (1924) |
| SemIf-2B | Dynamic | secondary | +7.02 [+4.21, +9.64] (4120) | +1.35 [-1.06, +3.62] (4120) |
| SemIf-2B | MHS | secondary | +40.07 [+37.23, +42.69] (3203) | +4.17 [+1.88, +6.38] (3203) |
| SemIf-2B | HateXplain | secondary | +19.02 [+14.96, +23.54] (1924) | +16.43 [+12.51, +20.55] (1924) |
| Nimble NF4 | Dynamic | secondary | +2.33 [+0.39, +4.27] (4120) | +6.08 [+4.03, +8.13] (4120) |
| Nimble NF4 | MHS | secondary | +3.45 [-0.28, +6.98] (3203) | +6.85 [+3.83, +9.85] (3203) |
| Nimble NF4 | HateXplain | secondary | +21.65 [+17.27, +25.88] (1924) | +20.00 [+15.76, +24.25] (1924) |
| BART | Dynamic | secondary | +11.74 [+8.91, +14.39] (4120) | +7.96 [+4.91, +10.89] (4120) |
| BART | MHS | secondary | +32.57 [+29.43, +35.91] (3203) | +32.57 [+29.43, +35.91] (3203) |
| BART | HateXplain | secondary | +24.71 [+20.83, +28.47] (1924) | +24.51 [+20.52, +28.36] (1924) |

Luna Decisions Dynamic and HateXplain retain the 199-validation-output post-hoc sensitivity designation. Inclusion in the primary family does not make them confirmatory. The original threshold-control families and frozen thresholds are retained.

## Corrected model–text pairs

Each identifier below is a model–text pair with matched A wrong and B correct against the final reference. A trailing `*` means all B components match; `?` means the component reference is unresolved. Unmarked pairs have at least one component mismatch.

- jev: `T5a26bbfa4c36`*, `T55c6f613b1af`*.
- laya: `T4cf1b22e9d9b`, `T07937f0ea253`, `T5c0acb1a1d9c`, `T15fd6bea0e46`, `T849cdaf5f08c`, `T023fa7075a0a`, `Te6c1d6ecb02e`, `T5458d11ae257`*, `Tcaf7be480d20`*, `Tfe26cda766b8`?, `T095d758e40d8`, `T52ebeb31f010`*, `T9603e5de48fc`*, `T88a6b715e066`*, `Taca335de5747`*, `Ta024c1cde369`, `T59417364b4fe`, `T5ce14526f390`, `T0088b26343cc`.
- decider: `Tf853c20fbf32`, `T849cdaf5f08c`, `T023fa7075a0a`*, `T9fe2b5a00938`*, `T37360a14d52d`, `T6081be1b3af3`*, `T1a6344e60c81`?, `Te68a3defd1dd`*, `Ta811b68b352c`, `Tfce63747ea4e`, `T095d758e40d8`, `T52ebeb31f010`*, `Tc751e3de774c`*, `T3caa31592539`, `Ted2aa6826759`*, `T7b6c5a2f212d`, `Ta024c1cde369`, `Tf56416b88130`, `Tafe80ef01e67`, `T5ce14526f390`, `T7d126895cde9`.
- qwen2b: `T4cf1b22e9d9b`, `T3e8ef89bca27`, `T15fd6bea0e46`, `T849cdaf5f08c`, `T2aeab30dad71`, `Tf8effce0edbf`?, `T862b90dd90c3`, `T4c7f9852cf6e`, `T4f1dac307154`, `T69ed2b8990f4`*, `T936bfa117ea6`, `T2b0eb21728d1`*, `T9fe2b5a00938`*, `T0d120cf2d08a`*, `Te5c62f97c5fc`, `T6b5cdffc6928`?, `Td497d0271c25`, `T8af1754fabca`, `T7ca607795247`, `T36ff0016820a`*, `Tf052ab5b675f`, `Td1487d1b7af3`, `T095d758e40d8`, `Ted2aa6826759`*, `Tb9e7a8a5b7d8`*, `T7b6c5a2f212d`, `T6744174c560d`*, `T8a1e4e08ebf0`*, `T804297a09845`*, `Taca335de5747`, `Ta024c1cde369`, `Te059f29ce8a5`, `T948fa34193e0`*, `T10e1eacb610b`*, `T59417364b4fe`, `Tf56416b88130`, `T5e9ba96adcd2`, `T5ce14526f390`, `T8c00a7b3a6db`*, `T7d126895cde9`, `T1b7b557a8714`, `T44c9ee329e5e`, `Td1983e82dcf9`.
- qwen4b: `T97ccd5576993`, `Taab21cef90b2`, `Taf8bfd945509`*, `T215a1e89dcfa`*, `T3e8ef89bca27`, `T5c0acb1a1d9c`, `T2aeab30dad71`, `Tfbe0e9937185`, `T6081be1b3af3`*, `T0d120cf2d08a`*, `Tbbfdcaf4c396`*, `Te68a3defd1dd`*, `Tc6d623543e9d`?, `Te925190b68e7`*, `Tc972ce9b126b`*, `T52ebeb31f010`*, `Ted2aa6826759`*, `Taca335de5747`*, `T1b7b557a8714`.
- nimble: `T5dd95725e413`, `Taf9ba989c477`, `Tee1e75ec1701`*, `Td0c90ec500f1`, `T9fe2b5a00938`*, `T1a6344e60c81`?, `T538dbab0d0bb`*, `Te68a3defd1dd`*, `T7ca607795247`, `T3ac5d78cea5b`?, `T0b04884832e1`*, `Tc972ce9b126b`, `Tc1c31c09df41`, `T8cefedbca741`*.
- gpt6_luna_decisions: `T08942d0359e4`*, `Taf8bfd945509`, `T8286fb49202d`, `T266219a88a56`, `T68ff108efed0`*, `T88e1def842b9`, `T4bdb2c4bde1d`*, `T53d37815c409`*.
- cope: `T5cf47ee7315b`, `Tcaf7be480d20`*, `T1d8428adb6a0`*.
- bart: `Ta75426a31105`.
- luna: `Td0c3cd153300`*, `T1cac81e52c7b`*, `T90b9884d899c`*, `T538dbab0d0bb`*, `T039a63a5ee69`*, `T8974b72fd9f4`*, `T52ebeb31f010`.
- sol: `T039a63a5ee69`*, `Tf2b87f8a4ca0`*, `T0c564709d532`*.

## Annotation file

`../data/audit/audit_annotations.csv` has one row per audited text. Columns: `audit_id`, `item_id`, `dataset`, `policy_id`, `stratum`, `weight`, `dataset_label`, `expert_policy`, `expert_components`, `opus_policy`, `opus_components`, `gemini_policy`, `gemini_components`, `reference_policy`, `reference_components`.

Component fields use `question=answer` pairs separated by semicolons. `uncertain` and `missing` preserve nonvotes; `unresolved` marks a reference without two agreeing definite votes. Texts and rationales are not redistributed. Use item IDs with the original datasets. Agreement is conditional on the resolved audit sample, not full-population human accuracy. Existing model result files are unchanged.
