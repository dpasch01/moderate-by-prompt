# Threshold controls: A* and B*

Paper reference: Section 4.3, Appendix H, Table 7. The [CSV](threshold_control.csv) contains all 24 model–dataset cells, full-precision scores, frozen thresholds, paired sample sizes and adjusted intervals. This export preserves the saved results; it introduces no inference or refitting.

## Conditions and tuning protocol

**A** is matched direct classification with definition, rule and glossary. **B** is decomposed classification with component questions and the fixed logical rule. **A*** thresholds A's hate option score; **B*** jointly thresholds B's binary component yes scores. These are the matched A/B conditions, not benchmark direct. BART here uses the policy-conditioned matched NLI formulation, not its definition-free benchmark baseline. See [component questions and rules](../prompts/decomposition_questions.md) and [instructions](../prompts/instructions.md).

The full test populations are Dynamic (4,120), MHS (3,203), and HateXplain (1,924; Davidson proxy). HateCheck is excluded because it has no development split. Tuning uses the same frozen 200 development IDs per dataset, never test labels. Primary models are Laya, SemIf/Qwen3.5-4B, Jev and GPT-6 Luna Decisions; exploratory models are Decider, SemIf/Qwen3.5-2B, Bespoke-Nimble NF4 and BART. CoPE and label-only commercial models are excluded for lack of usable option scores.

For A*, candidates are the distinct valid development hate scores, 0.5, and the next representable value below the minimum score. Select the threshold maximizing fixed-label binary macro-F1, breaking ties by distance to 0.5, then the larger threshold. Predict hate iff score **> threshold**; equality is non-hate. The primary thresholds were reused unchanged; the exploratory thresholds were selected and frozen before their test evaluation.

For B*, construct the same candidate set for each binary component and search all threshold combinations jointly to maximize final-verdict development macro-F1. Ties minimize the sum of absolute distances to 0.5, then prefer larger thresholds lexicographically in the frozen component order. Dynamic tunes scope then intentional, retaining the cached conduct argmax. MHS and HateXplain tune targeting then abuse. Predict yes iff score **> threshold**; equality is no. The unchanged Dynamic rule is intentional=yes AND (conduct=support OR (scope=yes AND conduct!=none)); MHS/HateXplain require targeting=yes AND abuse=yes. All B* thresholds were frozen and hashed before computing B* test metrics. Existing full-test component scores were reused, with no new test inference. B* is a new validation-tuned control after earlier test results were known, not a claim of historical preregistration.

Luna Decisions A* thresholds on Dynamic and HateXplain retain their **199-output post-hoc sensitivity** status. B* has 199 valid development outputs on Dynamic owing to one refusal; its other development cells have 200. Refusals/invalid answers are abstentions, never relabeled or imputed. Standalone F1 uses valid outputs; each contrast uses its paired valid intersection.

## Statistical families

Saved paired linked-cluster percentile bootstrap intervals use 10,000 draws, seed 20260929, and fixed binary labels. Linked texts remain together. For A*, primary and exploratory families each contain 4 models × 3 datasets × 2 contrasts = **24 contrasts** (A*−A and A*−B). For B*, two separate new families of **24** cover B*−A* and B*−B. Bonferroni adjustment is retained within each family for 95% familywise coverage (percentile tails 0.05/(2×24)). Thus there are four distinct 24-contrast families across the two stages; earlier families are not merged or changed.

## Full test results (24 cells)

F1 is on the 0–1 scale; differences and intervals are percentage points. Bold indicates an adjusted interval excluding zero. Differences use paired populations, so they need not equal subtraction of rounded standalone F1 values.

| Family | Model | Dataset | A | B | A* | B* | A*−A [adjusted interval] | A*−B [adjusted interval] | B*−A* [adjusted interval] | B*−B [adjusted interval] |
|---|---|---|---:|---:|---:|---:|---|---|---|---|
| primary | Laya | Dynamic | 0.654 | 0.533 | 0.649 | 0.654 | -0.44 [-1.00, +0.12] | **+11.64 [+9.40, +13.91]** | +0.49 [-1.45, +2.46] | **+12.13 [+9.95, +14.52]** |
| primary | Laya | MHS | 0.694 | 0.733 | 0.695 | 0.718 | +0.07 [-2.61, +2.95] | **-3.78 [-6.60, -0.95]** | +2.36 [-0.19, +4.98] | -1.42 [-3.84, +0.98] |
| primary | Laya | HateXplain | 0.722 | 0.768 | 0.781 | 0.782 | **+5.91 [+2.85, +8.93]** | +1.27 [-1.43, +4.02] | +0.10 [-2.63, +2.67] | +1.37 [-0.40, +3.37] |
| primary | SemIf/Qwen3.5-4B | Dynamic | 0.675 | 0.656 | 0.719 | 0.705 | **+4.31 [+2.56, +6.10]** | **+6.31 [+4.29, +8.41]** | -1.32 [-2.86, +0.23] | **+4.98 [+3.52, +6.45]** |
| primary | SemIf/Qwen3.5-4B | MHS | 0.718 | 0.683 | 0.710 | 0.718 | -0.89 [-3.32, +1.38] | **+2.67 [+0.49, +4.91]** | +0.86 [-0.99, +2.70] | **+3.53 [+1.67, +5.42]** |
| primary | SemIf/Qwen3.5-4B | HateXplain | 0.675 | 0.677 | 0.724 | 0.697 | **+4.96 [+1.69, +8.09]** | **+4.69 [+1.70, +7.67]** | **-2.71 [-4.92, -0.38]** | +1.98 [-1.70, +5.28] |
| primary | Jev | Dynamic | 0.826 | 0.842 | 0.852 | 0.821 | **+2.59 [+1.50, +3.76]** | +0.98 [-0.05, +2.05] | **-3.11 [-4.40, -1.93]** | **-2.13 [-3.10, -1.19]** |
| primary | Jev | MHS | 0.689 | 0.681 | 0.690 | 0.671 | +0.12 [-1.95, +2.10] | +0.92 [-1.06, +2.91] | **-1.92 [-3.67, -0.13]** | -1.00 [-2.62, +0.45] |
| primary | Jev | HateXplain | 0.721 | 0.713 | 0.755 | 0.720 | **+3.45 [+0.39, +6.68]** | **+4.25 [+0.95, +7.56]** | **-3.57 [-5.54, -1.59]** | +0.68 [-2.91, +4.38] |
| primary | GPT-6 Luna Decisions | Dynamic | 0.656 | 0.763 | 0.774 | 0.768 | **+11.78 [+9.84, +13.65]** | +1.21 [-0.36, +2.82] | -0.64 [-2.22, +0.99] | +0.56 [-0.30, +1.47] |
| primary | GPT-6 Luna Decisions | MHS | 0.608 | 0.581 | 0.623 | 0.629 | **+1.57 [+0.29, +3.06]** | **+4.26 [+2.05, +6.47]** | +0.53 [-1.96, +3.12] | **+4.79 [+2.21, +7.41]** |
| primary | GPT-6 Luna Decisions | HateXplain | 0.775 | 0.745 | 0.770 | 0.753 | -0.45 [-2.06, +1.06] | **+2.55 [+0.41, +4.68]** | -1.69 [-3.87, +0.46] | +0.85 [-0.85, +2.57] |
| exploratory | Decider | Dynamic | 0.585 | 0.554 | 0.689 | 0.692 | **+10.34 [+8.08, +12.82]** | **+13.50 [+10.90, +16.04]** | +0.35 [-1.47, +2.24] | **+13.85 [+11.52, +16.15]** |
| exploratory | Decider | MHS | 0.800 | 0.707 | 0.805 | 0.763 | +0.48 [-1.33, +2.19] | **+9.75 [+6.82, +12.75]** | **-4.21 [-6.51, -1.85]** | **+5.53 [+2.36, +8.59]** |
| exploratory | Decider | HateXplain | 0.656 | 0.687 | 0.695 | 0.704 | **+3.92 [+0.30, +7.62]** | +0.86 [-2.50, +4.27] | +0.88 [-2.27, +3.98] | +1.73 [-0.43, +3.87] |
| exploratory | SemIf/Qwen3.5-2B | Dynamic | 0.479 | 0.536 | 0.549 | 0.535 | **+7.02 [+4.21, +9.64]** | +1.35 [-1.06, +3.62] | -1.37 [-3.47, +0.77] | -0.02 [-1.60, +1.47] |
| exploratory | SemIf/Qwen3.5-2B | MHS | 0.220 | 0.579 | 0.620 | 0.649 | **+40.07 [+37.23, +42.69]** | **+4.17 [+1.88, +6.38]** | **+2.87 [+0.70, +5.07]** | **+7.04 [+4.52, +9.54]** |
| exploratory | SemIf/Qwen3.5-2B | HateXplain | 0.418 | 0.444 | 0.608 | 0.594 | **+19.02 [+14.96, +23.54]** | **+16.43 [+12.51, +20.55]** | -1.35 [-4.17, +1.46] | **+15.08 [+11.51, +18.48]** |
| exploratory | Bespoke-Nimble NF4 | Dynamic | 0.742 | 0.705 | 0.765 | 0.730 | **+2.33 [+0.39, +4.27]** | **+6.08 [+4.03, +8.13]** | **-3.57 [-5.37, -1.66]** | **+2.51 [+1.45, +3.60]** |
| exploratory | Bespoke-Nimble NF4 | MHS | 0.585 | 0.551 | 0.619 | 0.681 | +3.45 [-0.28, +6.98] | **+6.85 [+3.83, +9.85]** | **+6.24 [+3.33, +9.22]** | **+13.09 [+10.28, +15.82]** |
| exploratory | Bespoke-Nimble NF4 | HateXplain | 0.512 | 0.529 | 0.729 | 0.700 | **+21.65 [+17.27, +25.88]** | **+20.00 [+15.76, +24.25]** | -2.86 [-6.02, +0.35] | **+17.14 [+13.78, +20.52]** |
| exploratory | BART | Dynamic | 0.355 | 0.393 | 0.472 | 0.506 | **+11.74 [+8.91, +14.39]** | **+7.96 [+4.91, +10.89]** | **+3.40 [+0.19, +6.71]** | **+11.36 [+8.77, +13.93]** |
| exploratory | BART | MHS | 0.196 | 0.196 | 0.522 | 0.536 | **+32.57 [+29.43, +35.91]** | **+32.57 [+29.43, +35.91]** | +1.37 [-1.47, +4.23] | **+33.95 [+30.71, +37.37]** |
| exploratory | BART | HateXplain | 0.240 | 0.242 | 0.487 | 0.496 | **+24.71 [+20.83, +28.47]** | **+24.51 [+20.52, +28.36]** | +0.94 [-3.18, +5.03] | **+25.46 [+21.29, +29.57]** |

Primary family: B* significantly exceeds A* in 0/12 cells and is significantly worse in 4/12. Exploratory family: B* significantly exceeds A* in 3/12 cells (SemIf-2B/MHS, Bespoke-Nimble/MHS, BART/Dynamic) and is significantly worse in 2/12. Other cells do not establish a difference; they do not demonstrate equivalence.

## Frozen thresholds

Threshold values are exported without display rounding. Dynamic conduct remains argmax.

| Model | Dataset | A* hate threshold | B* yes thresholds | A* validation N | B* validation N |
|---|---|---:|---|---:|---:|
| Laya | Dynamic | 0.522 | scope=0.3515; intentional=0.1115 | 200 | 200 |
| Laya | MHS | 0.8076 | targeting=0.8271; abuse=0.5307 | 200 | 200 |
| Laya | HateXplain | 0.8212 | targeting=0.3289; abuse=0.7642 | 200 | 200 |
| SemIf/Qwen3.5-4B | Dynamic | 0.22270013882530887 | scope=0.37754066879814546; intentional=0.5 | 200 | 200 |
| SemIf/Qwen3.5-4B | MHS | 0.7310585786300049 | targeting=0.29421497216298875; abuse=0.7549149868676283 | 200 | 200 |
| SemIf/Qwen3.5-4B | HateXplain | 0.8933094060543488 | targeting=0.679178699175393; abuse=0.8807970779778824 | 200 | 200 |
| Jev | Dynamic | 0.32 | scope=0.64; intentional=0.66 | 200 | 200 |
| Jev | MHS | 0.7 | targeting=0.66; abuse=0.5 | 200 | 200 |
| Jev | HateXplain | 0.83 | targeting=0.9; abuse=0.89 | 200 | 200 |
| GPT-6 Luna Decisions | Dynamic | 0.11 | scope=0.5; intentional=0.14 | 199 | 199 |
| GPT-6 Luna Decisions | MHS | 0.43 | targeting=0.07; abuse=0.6 | 200 | 200 |
| GPT-6 Luna Decisions | HateXplain | 0.62 | targeting=0.28; abuse=0.53 | 199 | 200 |
| Decider | Dynamic | 0.17675901512855383 | scope=0.18386393785476685; intentional=0.3063355088233948 | 200 | 200 |
| Decider | MHS | 0.62921389167226 | targeting=0.09871912674070055; abuse=0.8613948097617208 | 200 | 200 |
| Decider | HateXplain | 0.7513394951820374 | targeting=0.5716194936150464; abuse=0.6513548701194006 | 200 | 200 |
| SemIf/Qwen3.5-2B | Dynamic | 0.8807970779778824 | scope=0.46879062662624377; intentional=0.6224593312018546 | 200 | 200 |
| SemIf/Qwen3.5-2B | MHS | 0.9465966702001758 | targeting=0.46879062662624377; abuse=0.8670357598021707 | 200 | 200 |
| SemIf/Qwen3.5-2B | HateXplain | 0.9046505351008906 | targeting=0.5926665999540698; abuse=0.7772998611746912 | 200 | 200 |
| Bespoke-Nimble NF4 | Dynamic | 0.8807970779778824 | scope=0.5; intentional=0.8807970779778824 | 200 | 200 |
| Bespoke-Nimble NF4 | MHS | 0.9706877692486436 | targeting=0.022977369910025615; abuse=0.9399133498259924 | 200 | 200 |
| Bespoke-Nimble NF4 | HateXplain | 0.9706877692486436 | targeting=0.9046505351008906; abuse=0.9465966702001758 | 200 | 200 |
| BART | Dynamic | 0.831690562243619 | scope=0.7501869313446721; intentional=0.5 | 200 | 200 |
| BART | MHS | 0.8489721886966797 | targeting=0.7725306519111796; abuse=0.7577943688959723 | 200 | 200 |
| BART | HateXplain | 0.7181992698789078 | targeting=0.8074606416386174; abuse=0.7457688450813293 | 200 | 200 |

## Valid and paired sample sizes

The four rightmost columns are contrast-specific paired N, in the same order as the results table.

| Model | Dataset | A N | B N | A* N | B* N | A*−A N | A*−B N | B*−A* N | B*−B N |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Laya | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| Laya | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| Laya | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| SemIf/Qwen3.5-4B | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| SemIf/Qwen3.5-4B | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| SemIf/Qwen3.5-4B | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| Jev | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| Jev | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| Jev | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| GPT-6 Luna Decisions | Dynamic | 4098 | 4118 | 4098 | 4118 | 4098 | 4098 | 4098 | 4118 |
| GPT-6 Luna Decisions | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| GPT-6 Luna Decisions | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| Decider | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| Decider | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| Decider | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| SemIf/Qwen3.5-2B | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| SemIf/Qwen3.5-2B | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| SemIf/Qwen3.5-2B | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| Bespoke-Nimble NF4 | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| Bespoke-Nimble NF4 | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| Bespoke-Nimble NF4 | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |
| BART | Dynamic | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 | 4120 |
| BART | MHS | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 | 3203 |
| BART | HateXplain | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 | 1924 |

## B* validation accounting

Hosted validation cost was **$0.11 for 1,200 requests**, rounded from $0.1085351 recorded or conservatively reserved. Jev made 600 requests, all valid, with $0.0344 recorded charges. Luna Decisions made 600 requests: 599 valid and one refusal, with $0.0730486 recorded charges and a retained $0.0010865 reservation for the unrecorded refusal charge. Recorded charges alone sum to $0.1074486; the reservation is not a confirmed charge.

The six local models produced another 3,600 validation outputs. Local cost remains unassigned, not zero. Eighteen local warm-up calls are excluded from validation results. No paid test predictions were added. These costs concern B* validation only, not historical A* tuning or the full test evaluations.
