# Selective Routing (Exploratory, Earlier Cohorts)

This exploratory analysis preceded the cascade evaluation in `cascades.md` and uses cached predictions on earlier 800-text cohorts per dataset, not the full test sets.

## Protocol

We retained Laya's direct answer except for a fixed fraction of texts with the smallest Laya probability margins, which instead received a commercial model's direct answer. Referral fractions were not selected on development data, and cascade latency was not measured end to end.

## Results

| Referral (20%) to | Dynamic | MHS | HateXplain |
|---|---:|---:|---:|
| None (Laya alone) | .658 | .696 | .730 |
| GPT-6 Sol | .729 | .721 | .763 |
| GPT-5.6 Luna | - | - | .714 |

Referring 20% of texts to Sol raises macro-F1 on all three datasets, whereas referring the same fraction to Luna lowers HateXplain to .714. Values for Luna on Dynamic and MHS were not reported in this analysis.
