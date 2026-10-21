# Validation of the Policy Contrast Set

The final validation uses one expert hate-speech researcher, Opus (`anthropic/claude-opus-5.5`), and Gemini (`google/gemini-4-argon`). This is mixed expert–LLM validation. Expected labels are researcher-defined hypotheses for the constructed examples, not inherited HateCheck gold labels.

The expert workbook and judge request messages omitted expected labels and model outputs. The human workbook randomized item order separately for each policy and quality sheet. Both LLM runs used the same deterministic SHA256 job ordering with seed 20260929; they did not use separate model-specific permutations. Every LLM request used fresh context. Policies were assessed separately.

The frozen rule accepts a text when at least two voters independently match the expected answer under BOTH policies, and at least two judge BOTH grammar and clarity yes. Uncertain/missing responses do not support acceptance. Requiring the same two voters to satisfy all four answers gives the identical accepted set here. No labels were repaired, and no rejected text was replaced.

## Agreement with expected labels (all 240 candidates)

The denominator includes all candidates; uncertain/missing answers are not agreements. Both means the expected pair is matched under both policies. Grammar/clarity columns count yes responses, not agreement with a policy label.

| Annotator | P_in | P_out | Both policies | Grammar yes | Clarity yes | Uncertain P_in / P_out |
|---|---:|---:|---:|---:|---:|---:|
| Expert | 240/240 (100.0%) | 240/240 (100.0%) | 240/240 | 240/240 | 240/240 | 0 / 0 |
| Opus | 234/240 (97.5%) | 240/240 (100.0%) | 234/240 | 240/240 | 237/240 | 4 / 0 |
| Gemini | 226/240 (94.2%) | 235/240 (97.9%) | 225/240 | 240/240 | 233/240 | 5 / 4 |

## Joint agreement

Fleiss kappa is calculated jointly across the expert and two judges on the full candidate set BEFORE exclusions. Primary values treat uncertain as an explicit nominal category, omitting missing ratings; the definite-only sensitivity omits an item if any voter is uncertain/missing. It is not an average of pairwise kappas.

| Outcome | N, uncertainty as category | Fleiss kappa | N, all definite | Fleiss kappa, definite-only |
|---|---:|---:|---:|---:|
| P_in | 240 | 0.891 | 231 | 0.963 |
| P_out | 240 | 0.971 | 236 | 0.994 |
| grammatical | 240 | undefined | 240 | undefined |
| clear | 240 | 0.189 | 240 | 0.189 |
| policies_pooled | 480 | 0.942 | 467 | 0.983 |

Grammar kappa is undefined because all ratings are yes. Agreement statistics are descriptive; two policy judgments on the same text are not independent observations.

## Acceptance

**234 of 240** candidates are accepted: **84 switch cases, 90 hateful controls, 60 neutral controls**. All 40 template clusters remain. The six exclusions are switch cases:

- `T0d374edb96f7feed`
- `T4632ba1dfda414c5`
- `T4dd07bb079dbd4ac`
- `T62bfe27bccaf127c`
- `T7291b3dad5031f15`
- `Td033a6ce833d4145`

All six lack two votes jointly supporting the expected policy pair; two also lack two joint positive quality judgments. All original judgments remain in annotations.csv.

## Model-result sensitivity

The cached model evaluation originally covered all 240 candidates. The final acceptance screen is a retrospective sensitivity; it does not claim that these 234 IDs were selected before the original inference. The original results.json remains byte-for-byte unchanged. The adjacent README gives 240-versus-234 results, counts, 95% cluster-bootstrap intervals and paired differences.

Bootstrap: 10,000 draws, seed 20260929; resample the 40 frozen template clusters, retaining linked templates and identity variants together. Shared multiplicities yield paired difference intervals. Refusal/failure/missing pairs count unsuccessful for correctness; false flips use two-valid-answer pairs. No between-model significance tests. The mixed reference may share model biases; it is not independent human-only ground truth.
