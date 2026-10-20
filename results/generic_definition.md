# Generic Definition (Early Experiments)

Early experiments supplied the same generic definition (`../prompts/definitions.md`), written for this study, to every dataset. No dataset is annotated under it, so agreement with the annotations cannot show whether models apply it correctly, and the paper excludes it from the main analysis.

The table reports its effect on binary macro-F1 relative to no definition, descriptively and without significance tests. As with the dataset-specific definitions, the effects are mixed in sign and vary with both the model and the dataset, from a loss of 8.3 points for SemIf-4B on Dynamic to a gain of 23.6 points for SemIf-2B on HateXplain. On HateXplain's three-class task, the generic definition and the Davidson proxy differ by at most 2.1 points for every decision model.

| Model | Binary ΔF1 Dynamic (pp) | MHS | HateXplain | HateCheck | HX-3 macro-F1, generic | HX-3 macro-F1, Davidson |
|---|---:|---:|---:|---:|---:|---:|
| Jev | −0.1 | −2.9 | +5.3 | +0.0 | .522 | .532 |
| Laya | −3.2 | +0.6 | +2.5 | −2.3 | .581 | .570 |
| Decider | +3.6 | −4.7 | −3.3 | +5.4 | .527 | .506 |
| SemIf-2B | −1.9 | +17.5 | +23.6 | +4.4 | .277 | .279 |
| SemIf-4B | −8.3 | −2.6 | +11.0 | −1.4 | .405 | .411 |
| Bespoke-Nimble | +3.6 | −3.1 | −0.4 | +0.3 | .377 | .372 |
| Luna Decisions | −1.9 | −8.1 | −0.3 | −4.6 | .593 | .612 |
| CoPE (NF4) | −0.7 | −3.4 | −2.5 | −1.7 | - | - |

HateXplain binary changes use an earlier 1,000-post sample. Three-class scores (HX-3) use the same 1,000 posts.
