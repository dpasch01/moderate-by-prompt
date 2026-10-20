# Policy Contrast Set

**Content warning.** This folder contains constructed hateful statements about identity groups. They exist only to test whether models follow a change in policy.

Dataset comparisons change texts and definitions together. This set holds the texts fixed and changes one sentence of the definition, which tells us whether a model's verdict follows the policy it is given (paper, Section 3 and Appendix K).

## Policies

- **P_in** is the frozen HateCheck definition in `../../prompts/definitions.md`.
- **P_out** is P_in with Dynamic's frozen sentence inserted directly after the list of protected characteristics:

  ```
  Men, white people and heterosexuals are explicitly out of scope as targets of the hate category.
  ```

All other benchmark-direct instructions (`../../prompts/instructions.md`) are identical under both policies.

Why this sentence: HateCheck's definition protects characteristics (sex, race, sexual orientation), so it covers men, white people, and straight people. Dynamic's definition protects only vulnerable or marginalized groups and excludes these three explicitly. Adding only Dynamic's exclusion sentence to the HateCheck definition makes the two policies differ in this one point, so a change in a model's verdict can be attributed to it.

## Texts

- 30 hateful HateCheck templates expressing an explicit attack on a single group (derogation, dehumanization, and threats).
- 10 neutral identity-mention templates.
- No templates with slurs, spelling variations, or multiple targets.
- Each template is filled with six identities: men, women, white people, Black people, straight people, gay people.
- Total: 240 texts (180 hateful, 60 neutral).
- Overlap with the HateCheck test set used in the main evaluation:
  - The 120 texts about men, white people, and straight people do not occur in it.
  - The 120 texts about women, Black people, and gay people match existing HateCheck test cases up to spacing, capitalization, and a final period (2 exact matches, 117 after ignoring spacing and case, all 120 after also ignoring a final period).
  - Each text is judged under both policies, so this does not affect the contrast.

| Type | Identities | Expected under P_in | Expected under P_out |
|---|---|---|---|
| Hateful, contested group | men, white people, straight people | hate | non-hate |
| Hateful, protected under both | women, Black people, gay people | hate | hate |
| Neutral | all six | non-hate | non-hate |

## Outcomes

- **Correct switch:** a hateful text about a contested group is classified hate under P_in and non-hate under P_out.
- **Controls correct:** a control text (hateful about a group protected under both policies, or neutral) is classified correctly under both policies.
- **False flip:** a text whose expected label does not change receives different labels under the two policies.

Refusals and missing answers count as failures. Intervals are 95% bootstrap intervals clustered by template.

## Results

Benchmark-direct classification under P_in and P_out, 480 independent decisions per model (240 texts × 2 policies), with the first policy balanced across texts. Every model returned valid answers for all 480 decisions. Cells are percentages with 95% bootstrap intervals clustered by template (10,000 draws, seed 20260929). No between-model significance tests.

| Model | Correct switch (N=90) | Hateful controls correct (N=90) | Neutral controls correct (N=60) | Hateful false flips | Neutral false flips |
|---|---:|---:|---:|---:|---:|
| Jev | 90.0 [84.4, 95.2] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 0/90 | 0/60 |
| Laya | 0.0 [0.0, 0.0] | 71.1 [60.4, 81.6] | 100.0 [100.0, 100.0] | 6/90 | 0/60 |
| Decider | 24.4 [17.6, 31.2] | 97.8 [94.3, 100.0] | 100.0 [100.0, 100.0] | 2/90 | 0/60 |
| SemIf-2B | 12.2 [5.4, 19.8] | 97.8 [94.4, 100.0] | 88.3 [69.0, 100.0] | 2/90 | 6/60 |
| SemIf-4B | 64.4 [52.7, 75.6] | 91.1 [82.9, 97.7] | 100.0 [100.0, 100.0] | 0/90 | 0/60 |
| Bespoke-Nimble | 46.7 [40.0, 54.5] | 97.8 [94.4, 100.0] | 98.3 [94.4, 100.0] | 1/90 | 1/60 |
| Luna Decisions | 71.1 [63.1, 78.9] | 96.7 [92.7, 100.0] | 100.0 [100.0, 100.0] | 1/90 | 0/60 |
| CoPE (NF4) | 57.8 [42.2, 72.9] | 100.0 [100.0, 100.0] | 70.0 [48.9, 86.1] | 0/90 | 4/60 |
| BART, no policy* | 0.0 [0.0, 0.0] | 100.0 [100.0, 100.0] | 96.7 [91.7, 100.0] | 0/90 | 0/60 |
| BART, policy-conditioned** | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 50.0 [28.6, 71.8] | 68/90 | 30/60 |
| GPT-5.6 Luna | 83.3 [75.8, 90.5] | 96.7 [92.7, 100.0] | 100.0 [100.0, 100.0] | 2/90 | 0/60 |
| GPT-6 Sol | 97.8 [94.3, 100.0] | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 0/90 | 0/60 |

\* Negative control. It receives no policy, so it cannot switch.
\*\* Auxiliary. Not reported in the paper.

False flips are counted among pairs with two valid answers.

`results.json` contains the full metrics with breakdowns by identity, identity pair, and HateCheck functionality.

### Hosted cost and latency

| Model | Requests | USD (total) | Median s | p95 s |
|---|---:|---:|---:|---:|
| Jev | 480 | 0.011 (estimate from usage) | 0.517 | 0.758 |
| GPT-5.6 Luna | 480 | 0.033 | 1.499 | 2.187 |
| GPT-6 Sol | 480 | 0.320 | 1.559 | 2.628 |
| Luna Decisions | 480 | 0.016 | 0.629 | 0.989 |

Local models ran in batches. Their timings are observed run distributions, not isolated latency measurements.

## Files

| File | Contents |
|---|---|
| `texts.csv` | `text_id`, `template`, `identity`, `type`, `text`, `expected_P_in`, `expected_P_out`. `template` is a display label. `text` is the exact evaluated string. |
| `annotations.csv` | Each annotator's judgment under each policy, the number of annotators matching the expected labels under both policies, the number judging the text grammatical and clear, and acceptance |
| `VALIDATION.md` | Validation protocol and results |
| `results.json` | Model results with breakdowns |
