# MHS definition-wording robustness

Benchmark-direct; 3,203 texts, ten models; BART excluded. Original predictions reused. Only the definition paragraph changes, including within CoPE's native wrapper.

| Model | Original F1 | P1 F1 | P2 F1 | Range (pp) |
|---|---:|---:|---:|---:|
| laya | 0.692 | 0.688 | 0.688 | 0.41 |
| decider | 0.794 | 0.786 | 0.784 | 1.08 |
| qwen2b | 0.442 | 0.430 | 0.426 | 1.61 |
| qwen4b | 0.725 | 0.712 | 0.728 | 1.57 |
| nimble | 0.616 | 0.596 | 0.604 | 1.99 |
| cope | 0.653 | 0.652 | 0.649 | 0.39 |
| jev | 0.689 | 0.693 | 0.695 | 0.62 |
| luna | 0.695 | 0.702 | 0.703 | 0.79 |
| sol | 0.698 | 0.683 | 0.697 | 1.45 |
| decisions | 0.658 | 0.648 | 0.655 | 1.00 |

| Model | Paraphrase | Difference pp [adjusted interval] | Changed / paired N | Changed % | Valid N |
|---|---|---|---:|---:|---:|
| laya | P1 | -0.41 [-1.43, +0.54] | 86/3203 | 2.68 | 3203 |
| laya | P2 | -0.40 [-1.27, +0.47] | 60/3203 | 1.87 | 3203 |
| decider | P1 | -0.80 [-1.87, +0.21] | 97/3203 | 3.03 | 3203 |
| decider | P2 | -1.08 [-2.01, -0.15] | 76/3203 | 2.37 | 3203 |
| qwen2b | P1 | -1.26 [-2.35, -0.20] | 122/3203 | 3.81 | 3203 |
| qwen2b | P2 | -1.61 [-2.56, -0.70] | 89/3203 | 2.78 | 3203 |
| qwen4b | P1 | -1.25 [-2.61, +0.08] | 153/3203 | 4.78 | 3203 |
| qwen4b | P2 | +0.33 [-0.94, +1.62] | 119/3203 | 3.72 | 3203 |
| nimble | P1 | -1.99 [-3.42, -0.56] | 253/3203 | 7.90 | 3203 |
| nimble | P2 | -1.24 [-2.46, +0.01] | 194/3203 | 6.06 | 3203 |
| cope | P1 | -0.13 [-0.92, +0.63] | 71/3203 | 2.22 | 3203 |
| cope | P2 | -0.39 [-1.26, +0.41] | 74/3203 | 2.31 | 3203 |
| jev | P1 | +0.41 [-0.75, +1.59] | 106/3203 | 3.31 | 3203 |
| jev | P2 | +0.62 [-0.46, +1.63] | 80/3203 | 2.50 | 3203 |
| luna | P1 | +0.66 [-0.83, +2.12] | 180/3203 | 5.62 | 3203 |
| luna | P2 | +0.79 [-0.64, +2.19] | 167/3203 | 5.21 | 3203 |
| sol | P1 | -1.45 [-3.01, +0.12] | 133/3203 | 4.15 | 3203 |
| sol | P2 | -0.08 [-1.64, +1.46] | 133/3203 | 4.15 | 3203 |
| decisions | P1 | -1.00 [-2.73, +0.64] | 122/3203 | 3.81 | 3203 |
| decisions | P2 | -0.32 [-2.24, +1.58] | 141/3203 | 4.40 | 3203 |

Paired linked-cluster bootstrap: 10,000 draws, seed 20260929, fixed binary labels, Bonferroni family of 20. Standalone scores exclude refusals; contrasts and changed percentages use paired valid outputs. Range is max-minus-min across all three conditions.

Spearman rho (ten model F1 rankings, average ranks for ties): {"original/P1": 0.9030303030303028, "original/P2": 0.9757575757575757, "P1/P2": 0.9515151515151514}. Correlations describe ranking stability; they are not an equivalence test.

Hosted accounting (USD; unknown charges retain conservative reservations):

```json
{
  "jev": {
    "requests": 6407,
    "recorded_usd": 0.121732,
    "recorded_or_reserved_usd": 0.124485,
    "unknown_charges": 1,
    "refusals": 0,
    "retries": 1
  },
  "luna": {
    "requests": 6408,
    "recorded_usd": 0.3507162,
    "recorded_or_reserved_usd": 0.3518252,
    "unknown_charges": 2,
    "refusals": 0,
    "retries": 2
  },
  "sol": {
    "requests": 6406,
    "recorded_usd": 3.345714,
    "recorded_or_reserved_usd": 3.345714,
    "unknown_charges": 0,
    "refusals": 0,
    "retries": 0
  },
  "decisions": {
    "requests": 6406,
    "recorded_usd": 0.1640955,
    "recorded_or_reserved_usd": 0.1640955,
    "unknown_charges": 0,
    "refusals": 0,
    "retries": 0
  }
}
```

Local cost is unassigned. Cached originals and paraphrase predictions come from separate sessions, so provider drift and execution variability can contribute. No historical result or manuscript was changed.

P1 was corrected with user approval before inference to preserve the prejudice requirement. Exact paragraphs are in [paraphrases.md](paraphrases.md); the rendered prompts and protocol remain frozen in the research archive. The protocol hash is recorded in results.json.

Two Luna requests (one provider-unavailable response and one timeout) and one Jev server-overload response were each retried once after review with identical payloads. All attempts and unknown-charge reservations remain in hosted accounting. See the three reviewed_*_amendment.json files.
