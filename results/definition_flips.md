# Prediction-Level Definition Effects

Effect of the dataset-specific definition relative to no definition, as percentages of texts. Summarized in Section 4.2 and Appendix E of the paper.

- **Ch.:** predictions that change.
- **Co.:** predictions that change from incorrect to correct.
- **Br.:** predictions that change from correct to incorrect.
- **ΔF1:** change in binary macro-F1, in percentage points.

Co. and Br. sum to Ch. For HateXplain, the definition is the Davidson proxy.

| Model | Dyn. Ch. | Dyn. Co. | Dyn. Br. | Dyn. ΔF1 | MHS Ch. | MHS Co. | MHS Br. | MHS ΔF1 | HX Ch. | HX Co. | HX Br. | HX ΔF1 | HC Ch. | HC Co. | HC Br. | HC ΔF1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jev | 8.7 | 4.1 | 4.6 | −0.5 | 10.6 | 5.2 | 5.4 | −2.7 | 8.0 | 6.4 | 1.6 | +4.5 | 2.8 | 1.4 | 1.4 | +0.1 |
| Laya | 11.6 | 3.8 | 7.8 | −4.4 | 8.0 | 5.1 | 2.9 | +1.1 | 9.4 | 6.2 | 3.1 | +2.6 | 8.0 | 2.5 | 5.5 | −2.8 |
| Decider | 9.5 | 6.1 | 3.4 | +3.3 | 4.5 | 1.8 | 2.7 | −1.0 | 11.6 | 2.8 | 8.8 | −5.4 | 15.6 | 11.4 | 4.1 | +5.8 |
| SemIf-2B | 19.1 | 7.9 | 11.2 | +0.7 | 7.1 | 3.0 | 4.2 | −1.2 | 27.8 | 22.0 | 5.8 | +18.8 | 6.3 | 2.8 | 3.5 | +1.5 |
| SemIf-4B | 20.9 | 7.1 | 13.8 | −7.2 | 16.3 | 11.6 | 4.7 | +4.1 | 20.2 | 15.4 | 4.8 | +8.9 | 11.6 | 4.6 | 7.1 | −0.8 |
| Bespoke-Nimble | 21.2 | 12.5 | 8.8 | +5.3 | 19.3 | 12.6 | 6.7 | +3.3 | 7.1 | 2.7 | 4.5 | −2.1 | 16.0 | 5.7 | 10.3 | −3.7 |
| Luna Decisions | 10.0 | 4.9 | 5.1 | −0.2 | 5.6 | 2.0 | 3.6 | −1.0 | 11.9 | 5.7 | 6.1 | −1.4 | 6.9 | 5.0 | 1.9 | +3.2 |
| CoPE (NF4) | 9.5 | 3.6 | 5.9 | −2.3 | 9.4 | 4.1 | 5.3 | −1.9 | 5.4 | 1.7 | 3.7 | −2.0 | 3.4 | 0.8 | 2.5 | −2.1 |
| GPT-5.6 Luna | 7.8 | 4.7 | 3.1 | +1.7 | 8.1 | 2.8 | 5.3 | −3.4 | 8.4 | 5.0 | 3.4 | +1.5 | 2.5 | 1.3 | 1.3 | +0.0 |
| GPT-6 Sol | 7.6 | 5.3 | 2.4 | +2.9 | 5.6 | 2.0 | 3.6 | -2.1 | 13.6 | 8.8 | 4.8 | +3.0 | 1.5 | 0.5 | 0.9 | -0.5 |

Percentages are rounded independently, so Co. + Br. can differ from Ch. by 0.1.

Sol uses the completed historical no-definition extension, compared with benchmark-direct dataset-specific definition predictions on the full cohorts (4,120 / 3,203 / 1,924 / 3,728 paired texts). See [exact counts and percentages](sol_definition_effects/prediction_flips.csv) and [four adjusted contrasts](sol_definition_effects/README.md). All earlier rows remain unchanged.
