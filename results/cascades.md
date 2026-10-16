# Cascades

## Protocol

Each cascade keeps the first model's answer and refers its least confident texts, ranked by the margin between its two option scores, to a second model.

- **Pairs:** seven pairs. Laya to Jev, Sol, Luna, or Luna Decisions, and Jev to Sol, Luna, or Luna Decisions.
- **Referral rates:** 0, 5, 10, 20, 30, 50, and 100%, all under the benchmark direct contract on the full test sets.
- **Frozen operating point:** for each pair and dataset, we froze one operating point before testing. It is the smallest rate within one point of the best macro-F1 on 200 labeled validation texts. HateCheck has no validation split, so its rate is transferred from the other three datasets.
- **Comparisons:** each frozen point is compared with the first model, the second model, and random referral of the same number of texts (1,000 random sets), in one family of 84 contrasts.
- **Cost:** combines recorded per-dataset charges, with Laya's local cost unassigned.
- **Latency:** simulated by adding the HateCheck median of the first model to that of the second, weighted by the referral rate.

## Results

- No frozen cascade is significantly better than both of its models.
- Confidence-based referral lies above random referral at most rates. The difference is significant only for Jev to Sol on Dynamic at 50% (2.7 points) and Jev to Luna on Dynamic at 5% (1.0 points), partly because 15 of the 28 frozen points refer all or no texts, where both referral policies coincide.
- On Dynamic, referring Jev's less confident half of the texts to Sol reaches .888, indistinguishable from Sol (.891), at about half its hosted cost ($0.35 versus $0.65 per 1K texts).
- On HateXplain, referring 20% of Laya's texts to Luna Decisions reaches .779, close to Sol (.784), at about 1% of Sol's cost.

## Figure

`../figures/cascade-curves.pdf` plots macro-F1 against simulated latency for cascades referring 0 to 100% of the first model's least confident texts (solid) or random texts (dotted, 95% range shaded). Markers show standalone models. The figure shows three of the seven pairs.
