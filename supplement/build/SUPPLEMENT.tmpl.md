---
title: "Supplementary Material"
subtitle: "Can Platforms Moderate by Prompt? Evaluating Structured Decision Models for Policy-Conditioned Hate-Speech Moderation"
---

This supplement accompanies the anonymous repository of the paper. It reports the tables, experiments and figures that the page limit excludes, and closes each section with what the results show. Section numbers and appendix letters refer to the submitted paper. All numbers are computed from the cached outputs in the repository, and no result here required new inference.

# S0 Reading Guide

**Conditions.** *No def.* gives the label names only. *Generic* adds one generic definition written for this study. *Bench.* (benchmark-direct) adds the dataset-specific definition and class descriptions. *A* (direct) and *B* (decomposed) add the fixed rule and the glossary of component questions, and differ only in the requested decision. *A\** and *B\** tune the direct threshold or the component thresholds on 200 labeled validation texts. *Soft* multiplies the component scores and tunes one threshold on the same texts.

**Statistics.** Macro-F1 is written as .xxx and differences in percentage points. Intervals come from the paired cluster bootstrap of Section 3.4 (10,000 draws, seed 20260929), with Bonferroni adjustment within the stated family. **Bold** differences have an adjusted 95% interval that excludes zero. The paper calls these significant, and calls the others inconclusive.

**Model names.** Luna is GPT-5.6 Luna and Sol is GPT-6 Sol. Luna Decisions is a separate decision model. Nimble is Bespoke-Nimble.

**Table S0.** Where each part of the supplement belongs in the paper, and what is new.

| Section | Paper | Content not in the paper |
|---|---|---|
| S1 Classification | 4.1, Table 2 | All five prompt conditions, hate precision and recall |
| S2 Generic definition | none | Effect of a generic definition |
| S3 Three-class task | 4.1 | Per-class F1 and offensive-language confusions |
| S4 Transfer and attributes | 4.1, 4.3, App. D | Transfer heatmap, per-class conduct and group F1 |
| S5 Definition effects | 4.2, Fig. 2 | Intervals, changed, corrected and broken predictions |
| S6 Ablation | 4.2, App. E | All 80 contrasts |
| S7 Prompt robustness | 4.2, App. F | Changed predictions and paraphrase wording |
| S8 Decomposition | 4.3, App. G | All 44 cells, soft rule, thresholds, corrected pairs, refusals |
| S9 Efficiency | 4.4, App. H | Latency and cost for every model and dataset |
| S10 Cascades | 4.4, App. I | All 28 frozen points, latency estimates, live run, routing |
| S11 Audit | 4.2, Table 3, App. J | Rater agreement, both references with intervals, disputed cases |
| S12 Policy contrast | 4.2, Table 3, App. K | Detection and adherence by identity, acceptance sensitivity |
| S13 Decider exposure | 4.1, App. L | Partition sizes and intervals |
| S14 Additional annotators | none | Guardrail annotation attempts |
| S15 Compute and spend | 3, App. C | Hardware and hosted spend |

# S1 Classification under All Prompt Conditions

The paper reports benchmark-direct macro-F1 (Table 2) and the A and B scores of the decomposition analysis. Tables S1a to S1d add the no-definition and generic conditions and the hate precision (P) and recall (R) behind each benchmark-direct score. Labeling every text non-hate scores {{N:nonhate_Dynamic}} on Dynamic, {{N:nonhate_MHS}} on MHS, {{N:nonhate_HateXplain}} on HateXplain and {{N:nonhate_HateCheck}} on HateCheck.

**Table S1a.** Binary macro-F1 on Dynamic (N = 4,120).

{{T:class_Dynamic}}

**Table S1b.** Binary macro-F1 on MHS (N = 3,203).

{{T:class_MHS}}

**Table S1c.** Binary macro-F1 on HateXplain (N = 1,924). †Generic was run only on the first 1,000 test posts in early experiments.

{{T:class_HateXplain}}

**Table S1d.** Binary macro-F1 on HateCheck (N = 3,728).

{{T:class_HateCheck}}

BART scores whether a text supports a sentence, so it has no separate no-definition run, and its benchmark-direct run is the policy-free baseline. Once the sentence contains a definition (Generic, A, B), BART labels almost every text hate, with hate recall of .96 to 1.00, and its macro-F1 falls to the level of labeling every text hate. The commercial LLMs were not run with the generic definition.

**What this shows.** Precision and recall explain several rankings in Table 2. On MHS, Decider combines the highest precision among the decision models (.615) with high recall (.830), whereas SemIf-2B reaches .980 recall at .302 precision, so it labels most comments hate. On Dynamic, Luna Decisions is the most precise decision model (.954) but recalls only .521. The prompt condition reorders models on every dataset, so no single prompt gives a stable ranking.

# S2 Generic Definition

Early experiments gave every dataset the same generic definition (repository, `prompts/definitions.md`). No dataset is annotated under it, so agreement with the labels cannot show whether a model applies it correctly, and the paper leaves it out. Table S2 reports its effect without significance tests.

**Table S2.** Change in binary macro-F1 (points) from adding the generic definition to the no-definition prompt. HateXplain uses the first 1,000 test posts.

{{T:generic}}

**What this shows.** A definition no dataset was annotated under still moves macro-F1 by up to {{N:gen_max}} points, in both directions, and the sign changes with the model and dataset. The definition-dependence of Section 4.2 is therefore not specific to the dataset-specific definitions.

# S3 Three-Class Task on HateXplain

**Table S3.** HateXplain three-class results under benchmark-direct classification (1,924 posts, 594 hate, 548 offensive, 782 normal). F1 and recall (R) per class, and the share of offensive posts labeled hate or normal. The supervised classifiers are trained on a 5,000-post subset of the training partition.

{{T:three}}

**What this shows.** Most models score lowest on the offensive class, and the out-of-the-box models move offensive posts mostly into hate. The decision models label {{N:off_lo}}% (Luna Decisions) to {{N:off_hi}}% (Bespoke-Nimble) of offensive posts hate, against 16% and 28% for the supervised classifiers, which instead confuse offensive with normal. Offensive-class F1 reaches at most .468 for the out-of-the-box models (Luna Decisions) and .471 for TF-IDF+LR. Separating offensive language from hate-speech is the weakest point of moderation by prompt.

# S4 Cross-Dataset Transfer and Attributes

![Macro-F1 of the supervised classifiers trained on one dataset (rows) and tested on each dataset (columns)](figures/supervised-transfer.png)

**Figure S1.** Macro-F1 of the supervised classifiers trained on one dataset (rows) and tested on each dataset (columns). Boxes mark the in-domain score.

**Table S4a.** Selected hyperparameters of the supervised classifiers, chosen on source-validation macro-F1.

{{T:transfer_hp}}

**Table S4b.** Attribute macro-F1 without a definition and with the dataset-specific definition (benchmark-direct). Group is HateCheck's referenced group (seven classes), direction is general or directed hate, and conduct is Dynamic's conduct type (six classes). The supervised classifiers are trained on Dynamic's conduct labels. CoPE and Sol were not run on attributes.

{{T:attr}}

**Table S4c.** Conduct-type F1 per class on Dynamic under benchmark-direct classification. Column headers give each class's share of the 3,356 test texts.

{{T:conduct}}

**Table S4d.** Referenced-group F1 per class on HateCheck under benchmark-direct classification.

{{T:group}}

**What this shows.** The supervised classifiers reach .70 to .82 in domain but lose up to 54 points elsewhere, and only training on Dynamic transfers to HateCheck. Within attributes, the decision models nearly solve group identification (.929 to .992), but not conduct. The three rare conduct classes (dehumanization, threatening, support) cover 4.5% of texts, and Jev is the only model above .38 on all three. Adding the definition raises conduct macro-F1 for every model with both runs and direction macro-F1 for five of eight, by up to 36 points (Jev, direction). This exceeds every binary effect in Table S5, so the definition matters more for attributes than for the binary task.

# S5 Definition Effects

The paper reports the 28 primary comparisons as a figure (Figure 2) and summarizes the changed predictions in one sentence. Table S5 gives every comparison with its adjusted interval and the predictions the definition changes, corrects and breaks. A corrected prediction is wrong without the definition and right with it, and a broken one the reverse. The family column gives the Bonferroni family size. Luna Decisions, Luna and Sol form separate families of 4 because they were added after the primary analysis.

**Table S5.** Benchmark-direct minus no-definition macro-F1 on the full test sets.

{{T:defeff}}

![Change in macro-F1 against the share of predictions the definition changes](figures/definition-flips.png)

**Figure S2.** Change in macro-F1 against the share of predictions the definition changes. Filled markers have adjusted intervals that exclude zero.

**What this shows.** In the primary family, {{N:de_gain}} comparisons are significant gains, {{N:de_loss}} significant losses and {{N:de_inc}} inconclusive. Macro-F1 understates how much a definition changes. Corrected and broken predictions offset each other, so SemIf-2B on Dynamic changes 19.1% of its predictions for a gain of 0.7 points, and Bespoke-Nimble on HateCheck changes 16.0% for an inconclusive loss. The largest net gains, for SemIf-2B and SemIf-4B on HateXplain, also come with the most changes. A platform cannot read a stable macro-F1 as evidence that a model ignores the definition.

# S6 Definition and Class-Description Ablation

The paper reports the ablation counts (Appendix E). Table S6 lists every contrast. C1 is the label-only prompt, C2 adds the definition, and C3 adds the class descriptions, which gives the benchmark-direct prompt. Scores are on texts valid under all three prompts. The nine decision and commercial models form one family of 72 contrasts and CoPE a family of 8.

**Table S6.** Ablation macro-F1 and adjusted differences (points).

{{T:ablation}}

**What this shows.** In the main family, the definition (C2 − C1) gives {{N:ab_def_gain}} significant gains and {{N:ab_def_loss}} losses in 36 contrasts, and the class descriptions (C3 − C2) {{N:ab_desc_gain}} gains and {{N:ab_desc_loss}} losses. The largest effects follow the definition, such as −27.3 points for SemIf-2B and +11.3 for SemIf-4B on MHS, and −11.1 for Luna Decisions on Dynamic. The class descriptions mostly move macro-F1 by less than two points, and partly reverse the definition's effect for SemIf-2B on MHS and HateXplain. CoPE loses with the definition on three datasets, consistent with its losses in Section 4.2.

# S7 Prompt Robustness

The paper reports the macro-F1 changes (Appendix F, Table 4). Table S7a adds the share of changed predictions and Table S7b their direction. Option-label variants rename the options to A and B (A/B) or reverse their order (Rev.), in a family of 10 contrasts. The paraphrases P1 and P2 replace the MHS definition, in a family of 20. All variants run on MHS under benchmark-direct classification.

**Table S7a.** Change in MHS macro-F1 (points) and share of changed predictions (%).

{{T:robust}}

**Table S7b.** Changed predictions per variant, split into corrected and introduced false positives (FP) and false negatives (FN).

{{T:robust_flips}}

The paraphrases were frozen before inference, and only the definition paragraph differs from the benchmark-direct MHS prompt.

> **Original.** Hate speech is prejudice-driven, hostile or malicious language directed at a person or group because of actual or perceived innate characteristics, particularly when the group is unnecessarily labeled. Assess whether the comment contains hate speech under this definition; the available judgments are yes, no, and unclear.
>
> **P1 (reordered clauses).** Language is hate speech when it targets a person or group because of their actual or perceived innate characteristics and is driven by prejudice and hostile or malicious, especially when it labels the group without need. Decide whether the comment contains hate speech under this definition; the possible judgments are yes, no, and unclear.
>
> **P2 (synonyms).** Hate speech is language motivated by prejudice that is hostile or malicious toward a person or group on the basis of real or assumed innate traits, in particular where the group is labeled needlessly. Determine whether the comment includes hate speech according to this definition; the judgments available are yes, no, and unclear.

Model rankings correlate at Spearman ρ of {{N:rho_o1}} (original and P1), {{N:rho_o2}} (original and P2) and {{N:rho_12}} (P1 and P2).

**What this shows.** Option names matter far more than definition wording. Renaming the options changes 44.5% of Laya's predictions, and reversing them 21.9% of Bespoke-Nimble's, while the paraphrases change at most 7.9% of any model's predictions. The paraphrases still change 1.9% to 7.9% of predictions, about as many as some dataset-specific definitions in Table S5, so part of each definition effect may reflect wording rather than content.

# S8 Decomposition

## S8.1 All Direct and Decomposed Comparisons

The paper summarizes 44 comparisons of direct (A) and decomposed (B) classification (Table 2, Figure 4). Table S8a lists them. Dynamic, MHS and HateXplain form the primary family of 30 contrasts, HateCheck a family of 10 and Luna Decisions a family of 4 on texts it answered under both conditions. ΔP and ΔR give the change in hate precision and recall in points. § marks the 3 comparisons in which A or B scores below labeling every text non-hate.

**Table S8a.** Decomposed minus direct macro-F1 on the same texts and definition.

{{T:decomp}}

In the primary family, decomposition gives {{N:dc_gain}} significant gains, {{N:dc_loss}} losses and {{N:dc_inc}} inconclusive results. Without the 3 marked comparisons, it gives {{N:dc_nd_gain}} gains and {{N:dc_nd_loss}} losses. On HateCheck it gives no gain and 3 losses, including −34.0 points for Decider, whose recall falls by 59 points.

## S8.2 Threshold Control and Soft Aggregation

The paper's Table 5 reports A, B, A\* and B\* with the B − A\* and B\* − A\* contrasts. Table S8b adds the soft rule and the effect of tuning itself. The primary family (P) holds Laya, SemIf-4B, Jev and Luna Decisions, and the exploratory family (E) the other four models, with adjustment within families of 24 contrasts. § marks the two Luna Decisions cells fitted post hoc on the 199 development texts with complete outputs.

**Table S8b.** Macro-F1 under each operating point, and adjusted differences (points).

{{T:thresh}}

**Table S8c.** Selected thresholds and validation macro-F1. B\* tunes one threshold per binary component, and Dynamic's conduct answer keeps the highest score.

{{T:thresh_sel}}

Tuning the direct threshold (A\* − A) gives {{N:th_aa}} significant gains in 24 comparisons, and tuning the components (B\* − B) {{N:th_bb}} gains. The soft rule beats A\* in {{N:th_sa_gain}} comparisons and loses in {{N:th_sa_loss}}, and beats B\* in {{N:th_sb_gain}} and loses in {{N:th_sb_loss}}.

## S8.3 Do Corrected Verdicts Rest on Correct Components?

Among the 200 audited texts (Section S11), decomposition corrects a direct verdict in 140 model-text pairs. Table S8d checks each corrected pair against the audit reference's component answers.

**Table S8d.** Audited model-text pairs that decomposition corrects, by whether every component answer matches the audit reference. Unresolved pairs have a component without a reference answer.

{{T:corrected}}

## S8.4 Luna Decisions Refusals

Luna Decisions refuses some requests, mostly on Dynamic and HateCheck (Table S8e). The paper excludes refusals. Table S8f recomputes the decomposition contrasts with refusals counted as hate or as errors, that is, as the label opposite to the gold label.

**Table S8e.** Luna Decisions requests and refusals by condition. Across all test conditions, including attributes and the three-class task, it refused 135 of 85,585 requests.

{{T:ref_cov}}

**Table S8f.** Luna Decisions decomposition contrasts under three treatments of refusals (adjusted within the family of 4).

{{T:ref_sens}}

**What this shows.** Decomposition is not a reliable improvement. Most of its gains come from cells where the direct prompt was badly calibrated, and a threshold tuned on 200 texts recovers them (A\* − A gains in 17 of 24 comparisons). Combining component scores softly does not help either, so the hard conjunctive rule is not what holds decomposition back. Of the 133 corrected pairs with resolved components, 73 rest on at least one wrong component, so decomposition often reaches the right verdict for the wrong reason. Treating refusals as hate or as errors changes no Luna Decisions result by more than 0.4 points, and no significance decision.

# S9 Efficiency

Figure 3 of the paper shows five models. Table S9a and Figure S3 cover every model on the same 3,728 HateCheck texts. Latencies are median and 95th-percentile complete-decision times in milliseconds, with one request at a time. Hosted cost is the recorded charge per 1K texts. \* marks local estimates, which price the measured serial throughput at \$0.20 per GPU-hour.

**Table S9a.** Quality, latency and cost of direct (A) and decomposed (B) classification on HateCheck.

{{T:eff_hc}}

![Macro-F1 against median latency (a) and cost per 1K texts (b) on HateCheck for every model](figures/quality-efficiency-all.png)

**Figure S3.** Macro-F1 against median latency (a) and cost per 1K texts (b) on HateCheck for every model. Filled markers show direct and hollow markers decomposed classification. Local costs are estimates at \$0.20 per GPU-hour.

**Table S9b.** Latency and cost on the other datasets. Jev, Laya, SemIf-4B and Sol were timed on a common sample of 800 texts per dataset, and the other models on the full test sets. Luna Decisions was timed with four concurrent requests and its cost is the recorded charge on the full test set. Luna was timed on only 100 texts per dataset and is omitted.

{{T:eff_other}}

Local models ran on one NVIDIA GeForce RTX 5070 Ti (16 GB), with batch size 1 and one request at a time. The local estimates apply the T4 rental rate to this GPU's throughput, so they price the GPU time our server needed rather than the time a T4 would need.

**What this shows.** Decomposition roughly doubles latency and local cost for SemIf, Bespoke-Nimble and CoPE. For Laya, Decider, Jev, Luna and Sol, median latency changes by at most 9% on HateCheck, but hosted cost still rises because each component is billed, by 47% to 139% for Jev and 89% to 196% for Luna Decisions. On Dynamic, CoPE answers the conduct question as six judgments, which raises its latency eightfold. Under direct classification every local model costs less per text than Jev, but only Jev, Luna Decisions and CoPE exceed .90 on HateCheck at under \$0.06 per 1K texts.

# S10 Cascades

Each cascade refers the first model's least confident texts to a second model, at a referral rate frozen on validation texts (Appendix I). Table S10a lists all 28 frozen points with their comparisons, from one family of 84 contrasts. TOST gives the 90% interval of the difference from the second model, and the last column of that cell states whether the interval lies within one point (≤1) or two points (≤2) of zero.

**Table S10a.** Frozen cascade operating points under benchmark-direct classification.

{{T:cascade}}

![Macro-F1 against expected latency at every referral rate](figures/cascade-curves.png)

**Figure S4.** Macro-F1 against expected latency at every referral rate. Dotted lines show random referral.

**Table S10b.** Estimated HateCheck latency at the frozen operating points. Each text adds the first model's measured time and, if referred, the second model's.

| Cascade | Referred texts | Median s | Mean s | 95th pct. s | Hosted \$ / 1K texts |
|---|---:|---:|---:|---:|---:|
| Jev→Sol | 1,864 / 3,728 | 1.467 | 1.118 | 2.194 | 0.348 |
| Jev→Luna | 746 / 3,728 | 0.335 | 0.558 | 1.451 | 0.036 |
| Jev→Luna Dec. | 186 / 3,728 | 0.327 | 0.356 | 0.550 | 0.024 |
| Laya→Jev | 3,728 / 3,728 | 0.371 | 0.388 | 0.461 | 0.022 |
| Laya→Sol | 3,728 / 3,728 | 1.525 | 1.608 | 2.157 | 0.652 |
| Laya→Luna | 3,728 / 3,728 | 1.021 | 1.098 | 1.523 | 0.068 |
| Laya→Luna Dec. | 3,728 / 3,728 | 0.297 | 0.333 | 0.489 | 0.032 |

To check the estimate, we ran Jev→Sol live on all HateCheck texts, one request at a time. It reached .976 macro-F1 at the same hosted cost (\$0.348 per 1K texts), with a median service time of 1.022 s against the estimated 1.467 s. The live run referred 1,789 of the 1,864 texts referred offline, and its labels agree with the cached labels on 99.7% of texts for Jev and 98.6% for Sol.

**Table S10c.** Exploratory routing from Laya to Sol under direct classification (A), on an earlier common sample of 800 texts per dataset. Corrected and introduced count the referred texts whose label Sol corrects or breaks.

{{T:routing}}

**What this shows.** Of the 28 frozen points, 15 refer all or no texts, where cascade and random referral coincide, and confidence-based referral is significantly better than random only twice. No cascade significantly exceeds its stronger model, so cascades buy cost, not quality. Jev→Sol on Dynamic and Laya→Luna Decisions on HateXplain are the useful cases, since both are equivalent to their stronger model within the stated margin at half or a fifth of its hosted cost. Routing more texts can also hurt. On MHS, sending every text from Laya to Sol lowers macro-F1 from .730 at 50% to .689, because Sol corrects 129 labels but breaks 96.

# S11 Policy and Component Audit

The audit reference for each judgment is the agreement of at least two of the expert and the two LLM judges (Appendix J). Table S11a gives agreement between raters on mutually definite answers, and Table S11b the model agreement behind Table 3 of the paper, with 95% cluster-bootstrap intervals, under the majority and under the expert alone.

**Table S11a.** Rater agreement on mutually definite answers, as agreeing/compared (Cohen κ). Component κ is not pooled across questions.

{{T:audit_pair}}

**Table S11b.** Model agreement with the audit reference (%, 95% interval). Agree uses the 187 resolved policy judgments, Conflicts the texts where the reference and the dataset label disagree (29 under the majority, 34 under the expert), and Comp. the texts whose component answers all resolve (180 and 187).

{{T:audit_models}}

**Table S11c.** Texts on which the reference conflicts with the dataset label (%, 95% interval), raw and reweighted by inverse inclusion probability.

{{T:audit_conf}}

The reweighted majority intervals in Table S11c use the same cluster bootstrap as the expert intervals. The paper's majority intervals (12% to 32% for MHS, 7% to 28% for HateXplain) instead poststratify each draw to the sampling strata, which narrows them.

**Table S11d.** Dynamic texts selected as disputed examples, with each rater's policy judgment. The dataset texts are not reproduced.

{{T:disputed}}

**What this shows.** The expert and both LLM judges agree on 94% to 96% of mutually definite policy judgments (κ .89 to .91). Disagreement concentrates in components, above all MHS abuse, where Gemini disagrees with both the expert and Opus (κ .30 and .29). Taking the majority therefore protects the reference against one judge's reading. Model agreement barely depends on the reference, as the expert-only and majority values differ by at most 10 points on the conflict texts and 4 points elsewhere, and the ranking is nearly the same (Spearman ρ .99). The expert alone finds similar or higher conflict rates on MHS and HateXplain (24% and 28% against 21% and 17%), so the label conflicts do not come from the LLM judges.

# S12 Policy Contrast

The policy contrast tests whether a model follows a controlled change of policy. P$_\text{in}$ is HateCheck's definition, and P$_\text{out}$ adds Dynamic's exclusion of men, white people and heterosexuals as hate targets. Each of the 90 switch texts should be hate under P$_\text{in}$ and non-hate under P$_\text{out}$, and the 150 controls should keep their label. The constructed texts are in the repository, behind a content warning.

**Table S12a.** Switch and control rates on all 240 texts (%), and the switch rate on the 234 texts accepted by the annotation rule (Appendix K). Intervals are bootstrapped over templates. False flips are controls whose label changes.

{{T:policy_main}}

**Table S12b.** Switch texts by targeted identity (30 each), as P$_\text{in}$ accuracy / switch rate among texts labeled hate under P$_\text{in}$ / switch rate among all texts (%).

{{T:policy_id}}

![Detection and adherence on the 90 switch texts](figures/policy-detection-adherence.png)

**Figure S5.** Detection and adherence on the 90 switch texts. The gap between detection and the switch among all texts shows texts that a model labels hate under P$_\text{in}$ but fails to switch.

**What this shows.** The policy contrast separates two failure modes. Jev, Sol and Luna Decisions switch 94% to 100% of the texts they label hate under P$_\text{in}$, and Luna 90%, so their misses come mostly from not labeling hate against men (P$_\text{in}$ accuracy 70% for Jev and 37% for Luna Decisions). Decider, SemIf-2B and BART label almost every switch text hate but rarely switch, so they ignore the policy change. Laya fails at both. Decider switches 73% of the texts about men it labels hate but none about white people, so adherence also varies by target. Accepting only the 234 validated texts changes switch rates by −1.5 to +6.4 points and leaves the ranking unchanged.

# S13 Decider Training Exposure

Replaying Decider's public training code on the MHS corpus assigns our MHS test comments to three partitions (Table S13a). The replay draws from {{N:replay_rows}} rows and {{N:replay_ids}} eligible comments, capping training at {{N:replay_cap}} comments.

**Table S13a.** Partitions of our MHS test set under the replayed training selection.

{{T:exp_split}}

**Table S13b.** Benchmark-direct macro-F1 on the 1,477 comments in neither partition. TF-IDF+LR and DistilBERT are trained on MHS.

{{T:exp_f1}}

**Table S13c.** Decider against the supervised classifiers on the same 1,477 comments.

{{T:exp_diff}}

**What this shows.** On comments outside the replayed selection, Decider still scores about 9 points above Jev and Sol but no better than classifiers trained on MHS. Its MHS lead is therefore in-domain training, not general ability.

# S14 Additional Annotators

To add a guardrail model to the annotation reference, we ran GPT-OSS Safeguard 20B and NVIDIA Nemotron Content Safety through OpenRouter on the audit and policy-contrast tasks on October 21, 2026.

**Table S14.** Attempted annotation runs. Recorded charges exclude reserved amounts for requests without a final charge.

| Model | Task | Requested | Attempted | Valid | Failed or invalid | Recorded \$ | Outcome |
|---|---|---:|---:|---:|---:|---:|---|
| GPT-OSS Safeguard 20B | Audit | 200 | 15 | 12 | 3 | 0.0021 | Rate limits, incomplete |
| GPT-OSS Safeguard 20B | Policy contrast | 720 | 44 | 42 | 2 | 0.0038 | Rate limits, incomplete |
| Nemotron Content Safety | Pilot, both tasks | 6 | 6 | 0 | 6 | 0.0012 | Invalid format, full run not started |

Safeguard returned 54 valid annotations, but repeated rate-limit errors stopped both tasks, including after a paced continuation and a bounded delay probe. Nemotron returned its native safe or unsafe ratings rather than the requested structured annotations, so all six pilot responses failed schema validation.

**What this shows.** Neither model produced a complete annotation reference, so the audit keeps the expert and two LLM judges. These are execution failures, not evidence about either model's accuracy on hate-speech.

# S15 Compute and Hosted Spend

Local models ran on one NVIDIA GeForce RTX 5070 Ti (16 GB) with an AMD Ryzen 9 5950X (16 cores) and 32 GB RAM, using torch 2.11 with CUDA 12.8. Decider, SemIf and BART ran in BF16, and Bespoke-Nimble and CoPE in NF4 with BF16 compute.

**Table S15.** Recorded hosted charges by experiment (USD). Ledgers were kept per experiment, so amounts are not summed across rows.

| Experiment | Jev | Luna Decisions | Luna | Sol |
|---|---:|---:|---:|---:|
| Main experiments, catalogued | {{N:cost_hist_jev}} | | {{N:cost_hist_luna}} | {{N:cost_hist_sol}} |
| Main experiments, later increment | {{N:cost_inc_jev}} | | {{N:cost_inc_luna}} | {{N:cost_inc_sol}} |
| All Luna Decisions runs | | {{N:cost_ld}} | | |
| Sol without definition | | | | {{N:cost_sol_nodef}} |
| Definition paraphrases | {{N:cost_par_jev}} | {{N:cost_par_ld}} | {{N:cost_par_luna}} | {{N:cost_par_sol}} |
| B\* validation | {{N:cost_bstar_jev}} | {{N:cost_bstar_ld}} | | |

**What this shows.** Hosted charges stay in the tens of dollars, and Sol accounts for most of them. Its benchmark-direct price per text is about ten times Luna's and thirty times Jev's.

# What the Supplement Adds

- **Rankings depend on the prompt.** No prompt condition gives a stable model ranking (S1), and even a generic definition moves macro-F1 by up to {{N:gen_max}} points (S2).
- **Definitions change more than macro-F1 shows.** Corrected and broken predictions offset each other (S5), the definition rather than the class descriptions drives the effect (S6), and option names matter more than definition wording (S7).
- **Offensive language remains the hardest boundary.** Decision models label up to {{N:off_hi}}% of offensive posts hate (S3).
- **Decomposition is an operating point, not an accuracy gain.** Threshold tuning recovers most of its gains, soft aggregation does not help, and many corrected verdicts rest on wrong components (S8).
- **Cost, not latency, separates the deployable options.** Decomposition raises hosted cost even where latency is flat (S9), and cascades save cost but never beat their stronger model (S10).
- **The audit does not hinge on the LLM judges.** The expert alone gives the same ranking and conflict rates (S11).
- **Policy failures have two causes.** Some models miss the target group, others ignore the policy change (S12).
- **Decider's MHS lead is in-domain training** (S13).
