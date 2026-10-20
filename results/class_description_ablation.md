# Class-Description Ablation

The paper's benchmark-direct prompt combines the dataset definition with class descriptions. This ablation separates the two. Summarized in Section 4.2 of the paper.

- **C1:** fixed task instructions and label names only.
- **C2:** C1 plus the frozen dataset definition paragraph.
- **C3:** C2 plus the class descriptions. This is the unchanged benchmark-direct prompt (Table 2, "Bench.").

C1 is **not** the paper's no-definition condition. On Dynamic, MHS, and HateCheck, C1 omits "Classify the text for hate speech." and joins the label list to the next sentence. On HateXplain, C1 keeps the hatespeech/offensive/normal-to-binary mapping, which the no-definition prompt omits. The two were run in different sessions, so their scores differ. For example, Jev on Dynamic scores .815 under C1 and .836 without a definition.

## Protocol

- All four full test sets, the same texts in all conditions.
- Paired cluster bootstrap with 10,000 draws (seed 20260929). Bonferroni adjustment within one family of 72 contrasts (9 models × 4 datasets × 2 adjacent contrasts).
- CoPE uses its native policy interface and forms a separate family of 8 contrasts. BART receives no policy, so its scores are identical across conditions.
- Comparisons use texts with valid outputs in all three conditions. Refusals are excluded, never counted as non-hate.

## Summary

| Contrast | Significant gains | Significant losses | Inconclusive |
|---|---:|---:|---:|
| Adding the definition (C2 − C1) | 10 | 10 | 16 |
| Adding class descriptions (C3 − C2) | 6 | 3 | 27 |

Counts cover the 36 categorical model and dataset cells. Jev, GPT-5.6 Luna, and GPT-6 Sol have no significant class-description effect. GPT-6 Sol's only significant contrast is a definition gain on Dynamic (+3.6 points).

## Macro-F1 (C1 / C2 / C3)

| Model | Dynamic | MHS | HateXplain | HateCheck |
|---|---|---|---|---|
| Laya | 0.680 / 0.623 / 0.639 | 0.677 / 0.701 / 0.692 | 0.718 / 0.753 / 0.753 | 0.744 / 0.717 / 0.709 |
| Decider | 0.649 / 0.610 / 0.624 | 0.750 / 0.812 / 0.794 | 0.626 / 0.597 / 0.611 | 0.763 / 0.769 / 0.780 |
| SemIf-2B | 0.503 / 0.590 / 0.584 | 0.664 / 0.390 / 0.442 | 0.586 / 0.486 / 0.548 | 0.619 / 0.696 / 0.656 |
| SemIf-4B | 0.690 / 0.687 / 0.652 | 0.610 / 0.723 / 0.725 | 0.571 / 0.645 / 0.692 | 0.785 / 0.799 / 0.786 |
| Bespoke-Nimble | 0.701 / 0.775 / 0.772 | 0.592 / 0.604 / 0.616 | 0.463 / 0.463 / 0.459 | 0.812 / 0.818 / 0.785 |
| Jev | 0.815 / 0.835 / 0.832 | 0.687 / 0.704 / 0.689 | 0.643 / 0.686 / 0.691 | 0.951 / 0.973 / 0.970 |
| GPT-5.6 Luna | 0.857 / 0.876 / 0.873 | 0.719 / 0.713 / 0.695 | 0.680 / 0.656 / 0.670 | 0.969 / 0.978 / 0.974 |
| GPT-6 Sol | 0.861 / 0.897 / 0.891 | 0.714 / 0.699 / 0.698 | 0.791 / 0.783 / 0.784 | 0.976 / 0.979 / 0.973 |
| Luna Decisions | 0.808 / 0.697 / 0.716 | 0.724 / 0.666 / 0.658 | 0.790 / 0.793 / 0.776 | 0.946 / 0.906 / 0.909 |
| CoPE (NF4) | 0.834 / 0.813 / 0.810 | 0.672 / 0.650 / 0.653 | 0.607 / 0.599 / 0.587 | 0.934 / 0.921 / 0.913 |
| BART* | 0.614 / 0.614 / 0.614 | 0.587 / 0.587 / 0.587 | 0.516 / 0.516 / 0.516 | 0.729 / 0.729 / 0.729 |

\* Policy-free control, identical in all conditions.

## Paired differences (percentage points, adjusted 95% interval)

Bold marks an adjusted interval that excludes zero. Differences use the three-way valid intersection, so they can differ slightly from subtracting the standalone scores.

| Model | Contrast | Dynamic | MHS | HateXplain | HateCheck |
|---|---|---|---|---|---|
| Laya | C2 − C1 | **-5.8** [-7.8, -3.8] | **+2.3** [+0.2, +4.4] | **+3.5** [+1.5, +5.6] | **-2.8** [-5.5, -0.1] |
| Laya | C3 − C2 | **+1.6** [+0.4, +2.9] | -0.8 [-2.4, +0.6] | -0.0 [-1.3, +1.2] | -0.8 [-2.1, +0.5] |
| Decider | C2 − C1 | **-3.9** [-5.9, -2.1] | **+6.2** [+3.9, +8.6] | **-3.0** [-4.9, -1.1] | +0.7 [-2.5, +3.7] |
| Decider | C3 − C2 | **+1.3** [+0.4, +2.3] | **-1.8** [-3.2, -0.4] | +1.4 [-0.1, +2.9] | +1.1 [-0.3, +2.6] |
| SemIf-2B | C2 − C1 | **+8.8** [+5.7, +11.9] | **-27.3** [-31.0, -23.3] | **-10.0** [-13.1, -6.9] | +7.7 [-1.1, +16.7] |
| SemIf-2B | C3 − C2 | -0.6 [-1.7, +0.4] | **+5.2** [+3.7, +6.8] | **+6.2** [+4.0, +8.7] | **-4.0** [-6.8, -1.7] |
| SemIf-4B | C2 − C1 | -0.2 [-2.9, +2.4] | **+11.3** [+8.6, +14.0] | **+7.4** [+4.8, +10.1] | +1.5 [-2.1, +5.3] |
| SemIf-4B | C3 − C2 | **-3.6** [-4.9, -2.2] | +0.2 [-1.7, +2.0] | **+4.7** [+2.1, +7.3] | -1.4 [-4.6, +1.8] |
| Bespoke-Nimble | C2 − C1 | **+7.3** [+4.8, +9.9] | +1.2 [-0.6, +3.0] | -0.0 [-2.2, +2.1] | +0.6 [-3.3, +4.2] |
| Bespoke-Nimble | C3 − C2 | -0.3 [-1.8, +1.3] | +1.2 [-0.7, +3.3] | -0.4 [-2.2, +1.3] | -3.3 [-7.6, +0.4] |
| Jev | C2 − C1 | +2.0 [-0.0, +3.9] | +1.7 [-0.5, +4.1] | **+4.3** [+2.4, +6.3] | +2.1 [-0.4, +4.1] |
| Jev | C3 − C2 | -0.3 [-1.0, +0.3] | -1.5 [-3.3, +0.1] | +0.5 [-0.6, +1.7] | -0.3 [-0.7, +0.0] |
| GPT-5.6 Luna | C2 − C1 | **+1.9** [+0.3, +3.6] | -0.7 [-3.1, +1.7] | **-2.4** [-4.6, -0.4] | +0.8 [-1.4, +2.5] |
| GPT-5.6 Luna | C3 − C2 | -0.4 [-1.5, +0.7] | -1.7 [-3.6, +0.0] | +1.4 [-0.5, +3.3] | -0.4 [-1.3, +0.7] |
| GPT-6 Sol | C2 − C1 | **+3.6** [+2.1, +5.0] | -1.5 [-3.5, +0.6] | -0.8 [-2.9, +1.3] | +0.3 [-0.6, +1.2] |
| GPT-6 Sol | C3 − C2 | -0.7 [-1.8, +0.3] | -0.1 [-2.0, +1.7] | +0.1 [-1.9, +2.0] | -0.6 [-1.5, +0.1] |
| Luna Decisions | C2 − C1 | **-11.1** [-13.3, -9.1] | **-5.8** [-8.8, -2.9] | +0.3 [-2.2, +3.0] | **-4.2** [-8.8, -1.1] |
| Luna Decisions | C3 − C2 | **+2.0** [+0.4, +3.4] | -0.7 [-2.8, +1.2] | -1.6 [-4.4, +0.8] | +0.5 [-0.5, +1.6] |
| CoPE (NF4) | C2 − C1 | **-2.1** [-3.4, -0.8] | **-2.2** [-3.6, -0.8] | -0.7 [-2.0, +0.6] | **-1.3** [-2.6, -0.2] |
| CoPE (NF4) | C3 − C2 | -0.2 [-0.9, +0.4] | +0.3 [-0.8, +1.4] | **-1.3** [-2.3, -0.3] | **-0.9** [-1.7, -0.3] |

CoPE intervals are adjusted within its own family of 8.

## Cost

New hosted runs for this ablation cost about $13.34. Jev cost is estimated from usage at its published rate. The other models' costs are recorded charges.
