# Change Log

## Completed Sol and wording robustness

- Added all four completed Sol historical no-definition contrasts and the Sol row in the Appendix E prediction-flip table, with exact counts and percentages. Earlier model rows are unchanged.
- Added the complete definition-effects Figure 2 (PDF/PNG) and replacement caption, including Sol under its separate four-comparison family.
- Added MHS prompt-wording robustness for ten models and two frozen paraphrases, with 20 Bonferroni-adjusted contrasts, ranking correlations and hosted accounting. BART is excluded; CoPE retains its native wrapper.
- Exported provenance without private research-tree locations; JSON artifacts contain no Windows path separators. Frozen research results remain unchanged.

## Threshold-control results

- Added `results/threshold_control.md` and `.csv` for Section 4.3, Appendix H, Table 7: matched A/B conditions, A*/B* tuning protocols, frozen thresholds, all 24 cells, valid/paired N and all 96 saved adjusted contrasts.
- Preserved separate primary and exploratory 24-contrast families for each tuning stage; documented the 199-output sensitivities and B* validation accounting ($0.11 recorded/reserved, 1,200 hosted requests).
- Added the results to the README contents table. Existing model results, predictions, prompts and thresholds are unchanged.

## Final annotation update

- Replaced the earlier annotation round following receipt of the final expert annotations and adoption of the expert–Opus–Gemini reference.
- Audit CSV now has the requested expert, Opus, Gemini and reference policy/component columns, with identifiers only.
- Audit protocol reports 187 resolved policy judgments, 180 all-component-resolved texts, expert–judge agreement, 29 reference–dataset conflicts, updated model agreement and component correctness, correction pairs, definition effects and paired intervals.
- Policy-contrast validation now documents per-annotator agreement with expected labels, Fleiss kappa, 234 accepted texts and six excluded IDs. Its README includes 240-versus-234 bootstrap sensitivity tables.
- No model result file, prediction, prompt or model configuration was changed. The original 240-candidate result file remains preserved; updated sensitivity estimates are documented separately.


## Second version

### Added

- `data/audit/audit_annotations.csv`: labels from the expert and two LLM judges, plus their majority reference, for all 200 audited texts. Texts are identified by dataset identifier only.
- `data/policy_contrast/`: the policy-contrast set. It contains the P_in and P_out policies, 240 constructed texts with expected labels, the expert and two LLM judges’ annotations, the validation report, and the model results (`results.json`, summary in `README.md`).
- `results/benchmark_direct.md` and `.csv`: benchmark-direct binary and three-class macro-F1 for all models.
- `results/luna_decisions_coverage.md`: Luna Decisions requests, refusals, and paired valid texts per condition.
- `results/definition_flips.md`, `results/attributes.md`, `results/three_class.md`: full tables that the paper's appendix now summarizes in text.
- `results/class_description_ablation.md`: ablation separating the definition from the class descriptions, with all 11 models.
- `CHANGELOG.md`.

### Updated

- `results/audit_protocol.md`: the final mixed reference uses one expert, Opus and Gemini; at least two agreeing definite votes are required. Added strata, annotator agreement, conflict intervals, per-dataset agreement, and a description of the annotation file.
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
