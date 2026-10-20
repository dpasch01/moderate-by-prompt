# Change Log

## Second version

### Added

- `data/audit/audit_annotations.csv`: labels from the three human annotators and the two GPT-6-Astra runs, plus the majority reference, for all 200 audited texts. Texts are identified by dataset identifier only.
- `data/policy_contrast/`: the policy-contrast set. It contains the P_in and P_out policies, 240 constructed texts with expected labels, the annotations of three annotators, the validation report, and the model results (`results.json`, summary in `README.md`).
- `results/benchmark_direct.md` and `.csv`: benchmark-direct binary and three-class macro-F1 for all models.
- `results/luna_decisions_coverage.md`: Luna Decisions requests, refusals, and paired valid texts per condition.
- `results/definition_flips.md`, `results/attributes.md`, `results/three_class.md`: full tables that the paper's appendix now summarizes in text.
- `results/class_description_ablation.md`: ablation separating the definition from the class descriptions, with all 11 models.
- `CHANGELOG.md`.

### Updated

- `results/audit_protocol.md`: the human annotation is complete. The reference is now the majority of three humans, and the GPT-6-Astra runs no longer vote. All results now come from the human reference. Added strata, annotator agreement, conflict intervals, per-dataset agreement, and a description of the annotation file.
- `settings/inference_settings.md`:
  - The hardware now follows the run metadata (RTX 5070 Ti and Ryzen 9 5950X, replacing T4 and Xeon).
  - Luna Decisions refusals are counted over test conditions (135 of 85,585).
  - Added the supervised training settings.
  - Added that validation data also select thresholds and cascade rates.
- `results/efficiency.md`: throughput is defined as texts divided by the sum of per-text timing intervals. Labeled as matched direct (A) and decomposed (B).
- `results/cascades.md`:
  - Latency is now estimated per text. Added a table of the estimates.
  - The Jev to Luna gain is now 0.9 points, and the 100,000-draw sensitivity check was added.
  - "Indistinguishable" is now "not significantly different".
  - Added the Laya-first latency estimates from a new Laya timing run, latency at every referral rate for all seven pairs, and the concurrency of the hosted stage timings.
  - Added a live serial run of the Jev to Sol cascade on HateCheck.
- `results/decider_exposure.md`: added a summary. The lower bound of the Decider A interval is now +0.1 (was +0.2). Its paper reference is now Section 5.
- `results/generic_definition.md`: three rounding corrections (.581, −1.4, .593).
- `data/policy_contrast/README.md`: added why the exclusion sentence is added to the HateCheck definition, and the overlap of the 240 texts with the HateCheck test set.
- `README.md`: new files and paper references. Removed the note about the audit being in progress.
