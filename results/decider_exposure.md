# Decider Training Exposure

Decider's public training recipe includes the Measuring Hate Speech (MHS) corpus. We replayed the recipe to determine which MHS test comments fall into its training selection.

## Protocol

- We replayed Decider's public training recipe (commit `e50e549`) unchanged on a pinned revision of the MHS corpus (`5468f6e`), recovering the comments its loader retains for training (20,000) and for evaluation (1,500).
- Our 3,203 MHS test comments split into 1,603 in the training selection (403 hate), 123 in the evaluation partition, and 1,477 in neither (350 hate).
- We compare macro-F1 on the training-selected comments (Seen) with the comments in neither set (Neither), using 10,000 cluster bootstrap draws (seed 20260929). Intervals are exploratory and not adjusted for multiplicity.
- Jev and Sol serve as references for the difficulty of the two subsets, although their own training data are undisclosed.
- The replay reflects the current recipe and cannot establish the exposure of the released weights, which were trained in stages.

## Results

| Model | Condition | Seen | Neither | Δ (pp) [95% CI] |
|---|---|---:|---:|---|
| Decider | Benchmark | .809 | .780 | +2.9 [−0.2, +6.1] |
| Decider | A | .817 | .784 | +3.3 [+0.2, +6.5] |
| Decider | B | .728 | .687 | +4.1 [+0.2, +8.2] |
| Jev | Benchmark | .686 | .691 | −0.5 [−4.2, +3.1] |
| Jev | A | .687 | .689 | −0.3 [−4.0, +3.4] |
| Jev | B | .677 | .684 | −0.8 [−4.4, +2.8] |
| GPT-6 Sol | Benchmark | .704 | .692 | +1.2 [−2.6, +4.9] |
| GPT-6 Sol | A | .685 | .680 | +0.5 [−3.4, +4.3] |
| GPT-6 Sol | B | .687 | .681 | +0.6 [−3.1, +4.3] |

Seen: N = 1,603. Neither: N = 1,477.

## Other training data

Decider's other hate and offensive-language training tasks (TweetEval hate and offensive, the Davidson et al. corpus, and ProsocialDialog) share no exact text with our four test sets. One HateCheck text matches after normalization.
