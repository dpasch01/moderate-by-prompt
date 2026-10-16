# Policy and Component Audit

Agreement with dataset labels does not show that a model follows the supplied definition. The audit labels a sample of test texts directly against each dataset-specific definition and its component questions.

## Sampling

- 50 test texts per dataset, sampled without replacement (seed 20260929).
- Per dataset, 40 texts whose prediction changed with the definition for at least one model, and 10 whose prediction did not. Each half is balanced on the binary gold label.
- Because the sample oversamples definition-sensitive texts, rates are reweighted by inverse inclusion probability. Raw agreements describe the enriched sample rather than the full test sets.

## Annotation

- Annotators saw an anonymous identifier, the text, the supplied definition, and the component questions, in shuffled order. They did not see the dataset name, gold label, or any model output.
- Each annotator gave a policy judgment (meets the definition or not) and an answer to every component question, or marked it uncertain.
- Two annotators are independent, fresh-context instances of GPT-6-Astra. They agreed on 177 of 178 texts where both gave a definite policy judgment.
- The third annotator is a human, and the reference is the majority of the three. **[Pending at submission.]**
- GPT-6-Astra comes from the same provider as GPT-5.6 Luna, GPT-6 Sol, and Luna Decisions, so their agreement with the reference may partly reflect shared model behavior. Agreement with each annotator is therefore reported separately below. **[Pending at submission.]**

## Measures

For each model, we report agreement with the reference on:

- **Policy:** benchmark direct predictions.
- **Conflicts:** the subset where the reference conflicts with the dataset label.
- **Components:** texts where all of the model's component answers match the reference.

## Results

All values are pending the human annotation and will be updated here.

| Model | Policy (%) | Conflicts | Components (%) |
|---|---:|---:|---:|
| Jev | 90 | 18/25 | 73 |
| Laya | 62 | 12/25 | 39 |
| Decider | 66 | 8/25 | 32 |
| SemIf-2B | 50 | 8/25 | 28 |
| SemIf-4B | 69 | 12/25 | 54 |
| Bespoke-Nimble | 68 | 14/25 | 57 |
| Luna Decisions | 79 | 13/25 | 59 |
| CoPE | 79 | 17/25 | 58 |
| BART* | 53 | 7/25 | 43 |
| GPT-5.6 Luna | 90 | 20/25 | 74 |
| GPT-6 Sol | 93 | 18/25 | 82 |

Policy agreement uses 177 texts, conflicts 25, and components 152. \* Policy-free direct baseline.

The reference conflicts with the dataset label on 1 of 46 Dynamic, 15 of 40 MHS, 10 of 43 HateXplain, and 0 of 48 HateCheck texts with a definite reference, or 2%, 22%, 25%, and 0% after reweighting.

## Agreement by annotator

To be added after the human annotation: each model's agreement with the human annotator alone and with each GPT-6-Astra run alone, and the rate at which the two GPT-6-Astra runs disagree.
