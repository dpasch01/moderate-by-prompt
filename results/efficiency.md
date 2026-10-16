# Efficiency Measurements

Complete-decision timing and recorded hosted cost on all 3,728 HateCheck texts, for direct (A) and decomposed (B) classification. A machine-readable version is in `efficiency.csv`.

## Protocol

- The time to a complete decision includes per-text execution and, for decomposition, all component answers and the rule computation. Model loading and warm-up are excluded.
- Texts are processed one at a time. Batch size and hosted concurrency are one.
- Observed throughput uses the complete elapsed processing time rather than the reciprocal of median latency, so it does not represent peak throughput.
- Hosted cost comes from recorded usage and charges. No monetary cost is assigned to local inference (shown as a dash, not zero cost).
- BART's timing reflects its definition-conditioned template.
- Hardware for local models is listed in `../settings/inference_settings.md`.

## Results

| Model | Median ms A | Median ms B | 95th pct. ms A | 95th pct. ms B | Texts/s A | Texts/s B | USD / 1,000 texts A | USD / 1,000 texts B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Jev | 335.6 | 342.9 | 536.9 | 622.1 | 2.56 | 2.37 | 0.033 | 0.054 |
| Laya | 48.3 | 52.5 | 92.6 | 93.9 | 18.68 | 17.49 | - | - |
| Decider | 133.6 | 134.6 | 292.5 | 264.9 | 6.31 | 6.45 | - | - |
| SemIf-2B | 125.3 | 250.5 | 272.1 | 540.4 | 6.56 | 3.28 | - | - |
| SemIf-4B | 183.7 | 343.8 | 325.4 | 555.6 | 4.82 | 2.63 | - | - |
| Bespoke-Nimble | 335.1 | 686.2 | 641.7 | 1,255.0 | 2.60 | 1.29 | - | - |
| Luna Decisions* | 242.8 | 290.8 | 573.3 | 655.2 | 3.42 | 2.96 | 0.057 | 0.113 |
| CoPE (NF4) | 266.2 | 533.4 | 276.5 | 549.2 | 3.75 | 1.87 | - | - |
| BART | 35.2 | 47.3 | 74.3 | 66.4 | 24.12 | 20.11 | - | - |
| GPT-5.6 Luna | 843.9 | 884.8 | 1,273.1 | 1,302.7 | 1.10 | 1.05 | 0.120 | 0.129 |
| GPT-6 Sol | 1,425.9 | 1,383.4 | 2,123.6 | 2,294.3 | 0.66 | 0.65 | 1.177 | 1.256 |

\* Timed in a later serving session, including refusals.
