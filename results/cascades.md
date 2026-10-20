# Cascades

## Protocol

Each cascade keeps the first model's answer and refers its least confident texts, ranked by the margin between its two option scores, to a second model.

- **Pairs:** seven pairs. Laya to Jev, Sol, Luna, or Luna Decisions, and Jev to Sol, Luna, or Luna Decisions.
- **Referral rates:** 0, 5, 10, 20, 30, 50, and 100%, all under benchmark-direct classification on the full test sets.
- **Frozen operating point:** for each pair and dataset, we froze one operating point before testing. It is the smallest rate within one point of the best macro-F1 on 200 labeled validation texts. HateCheck has no validation split, so its rate is transferred from the other three datasets.
- **Comparisons:** each frozen point is compared with the first model, the second model, and random referral of the same number of texts (1,000 random sets), in one family of 84 contrasts.
- **Cost:** combines recorded per-dataset charges, with Laya's local cost unassigned.
- **Latency:** estimated offline on HateCheck. For each text, the estimate adds the first model's measured time and, if the text is referred, the second model's measured time on the same text. Median, mean, and 95th percentile are computed over these per-text sums. The stages were timed in separate sessions, so this is not a measured live cascade, and orchestration overhead is not included. Hosted stage times come from the benchmark-direct runs: Jev with one outstanding request, Sol and Luna Decisions with four concurrent requests, and Luna mostly with four.

## Results

- No frozen cascade is significantly better than both of its models.
- Confidence-based referral lies above random referral at most rates. The difference is significant only for Jev to Sol on Dynamic at 50% (2.7 points) and Jev to Luna on Dynamic at 5% (0.9 points), partly because 15 of the 28 frozen points refer all or no texts, where both referral policies coincide.
- With 100,000 bootstrap draws instead of 10,000, the Jev to Luna difference becomes inconclusive (adjusted interval −0.01 to +1.93 points). Only Jev to Sol remains significant.
- On Dynamic, referring Jev's less confident half of the texts to Sol reaches .888, not significantly different from Sol (.891), at about half its hosted cost ($0.35 versus $0.65 per 1K texts).
- On HateXplain, referring 20% of Laya's texts to Luna Decisions reaches .779, close to Sol (.784), at about 1% of Sol's hosted cost.

## Estimated latency on HateCheck

| Cascade | Referred texts | Median s | Mean s | 95th pct. s | Hosted USD / 1K texts |
|---|---:|---:|---:|---:|---:|
| Jev to Sol | 1,864 / 3,728 | 1.467 | 1.118 | 2.194 | 0.348 |
| Jev to Luna | 746 / 3,728 | 0.335 | 0.558 | 1.451 | 0.036 |
| Jev to Luna Decisions | 186 / 3,728 | 0.327 | 0.356 | 0.550 | 0.024 |
| Laya to Jev | 3,728 / 3,728 | 0.371 | 0.388 | 0.461 | 0.022 |
| Laya to Sol | 3,728 / 3,728 | 1.525 | 1.608 | 2.157 | 0.652 |
| Laya to Luna | 3,728 / 3,728 | 1.021 | 1.098 | 1.523 | 0.068 |
| Laya to Luna Decisions | 3,728 / 3,728 | 0.297 | 0.333 | 0.489 | 0.032 |

Referral rates are the frozen operating points. Hosted cost sums the recorded charges of all first-stage requests and of the referred second-stage requests. Laya's local cost is unassigned. On HateCheck, every Laya-first frozen point refers all texts, so these estimates equal the second model's time plus Laya's.

Laya's per-text times come from a separate serial run (batch size 1, three warm-up calls excluded) on all 3,728 HateCheck texts:
- Median 0.040 s, mean 0.046 s, 95th percentile 0.091 s.
- 21.8 texts/s (texts divided by the sum of per-text intervals).

The cached predictions were produced with batch size 16. The batch-1 run changes 16 of 3,728 labels (maximum probability difference 0.086), so it is used for timing only. Referrals always follow the cached predictions.

## Live run: Jev to Sol on HateCheck

To check the offline estimate, we ran the Jev to Sol cascade live on all 3,728 HateCheck texts:
- serial, one outstanding request at a time, no retries;
- Jev on every text, then Sol on Jev's least confident 50% (1,864 texts), ranked by Jev's live option-score margin.

| Measure | Live run | Offline estimate |
|---|---:|---:|
| Median service time per text (s) | 1.022 | 1.467 |
| Mean service time per text (s) | 0.909 | 1.118 |
| 95th percentile (s) | 1.792 | 2.194 |
| Macro-F1 | .976 | - |
| Hosted cost (USD per 1K texts) | 0.348 | 0.348 |

- **Service time** is the sum of a text's stage request times. It excludes the wait in the serial queue, which depends only on how the run was scheduled.
- Live service times are lower than the estimate. The sessions differ, and the cached Sol times used for the estimate were recorded with four concurrent requests, so the cause of the gap is not isolated.
- Overlap and agreement with the cached run:
  - the referred texts overlap 1,789 of the 1,864 referred in the frozen analysis (Jaccard .92);
  - live labels agree with the cached labels on 99.7% of texts for Jev and 98.6% for Sol.
- Jev cost is estimated from usage at its published rate. Sol cost is the recorded charge.

### Estimated latency at every referral rate (HateCheck, median s / p95 s)

| Cascade | 0% | 5% | 10% | 20% | 30% | 50% | 100% |
|---|---:|---:|---:|---:|---:|---:|---:|
| Laya to Jev | 0.040 / 0.091 | 0.041 / 0.129 | 0.042 / 0.374 | 0.044 / 0.397 | 0.046 / 0.414 | 0.214 / 0.435 | 0.371 / 0.461 |
| Laya to Sol | 0.040 / 0.091 | 0.041 / 0.129 | 0.042 / 1.523 | 0.044 / 1.661 | 0.046 / 1.746 | 0.645 / 1.903 | 1.525 / 2.157 |
| Laya to Luna | 0.040 / 0.091 | 0.041 / 0.129 | 0.042 / 1.019 | 0.044 / 1.132 | 0.046 / 1.193 | 0.443 / 1.283 | 1.021 / 1.523 |
| Laya to Luna Decisions | 0.040 / 0.091 | 0.041 / 0.129 | 0.042 / 0.301 | 0.044 / 0.365 | 0.046 / 0.398 | 0.181 / 0.424 | 0.297 / 0.489 |
| Jev to Sol | 0.325 / 0.409 | 0.327 / 1.533 | 0.329 / 1.823 | 0.335 / 1.961 | 0.344 / 2.063 | 1.467 / 2.194 | 1.812 / 2.487 |
| Jev to Luna | 0.325 / 0.409 | 0.327 / 1.132 | 0.329 / 1.359 | 0.335 / 1.451 | 0.344 / 1.496 | 1.039 / 1.611 | 1.313 / 1.888 |
| Jev to Luna Decisions | 0.325 / 0.409 | 0.327 / 0.550 | 0.329 / 0.608 | 0.335 / 0.675 | 0.344 / 0.703 | 0.504 / 0.745 | 0.590 / 0.823 |

## Figure

`../figures/cascade-curves.pdf` plots macro-F1 against expected latency (HateCheck matched-direct stage medians weighted by the referral rate) for cascades referring 0 to 100% of the first model's least confident texts (solid) or random texts (dotted, 95% range shaded). Markers show standalone models. The figure shows three of the seven pairs.
