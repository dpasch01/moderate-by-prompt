# Definitions

Each dataset-specific definition is our source-grounded paraphrase of the criteria documented for the dataset. It is inserted verbatim into the instructions of the dataset-specific condition, together with the class descriptions in `instructions.md`.

## Dynamic

Paraphrased from the dataset's annotation guidelines and Vidgen et al. (2021).

```
Hate speech is abusive expression aimed at people because of group characteristics, including ethnic origin, religion, gender or sexuality. It includes explicit disparagement, implicit hostility, dehumanization, threats, and endorsement of hateful entities. The annotation codebook treats hate as intentional expression while acknowledging that intent can be difficult to infer. For this dataset, the target must be a vulnerable, marginalized or discriminated-against group. Men, white people and heterosexuals are explicitly out of scope as targets of the hate category. Relevant identities are open-ended and also include immigration status, nationality, disability and class. Classify content as hate or nothate using this dataset-specific scope.
```

## MHS

Paraphrased from the direct hate-speech survey item of Sachdeva et al. (2022).

```
Hate speech is prejudice-driven, hostile or malicious language directed at a person or group because of actual or perceived innate characteristics, particularly when the group is unnecessarily labeled. Assess whether the comment contains hate speech under this definition; the available judgments are yes, no, and unclear.
```

## HateXplain

HateXplain's annotation instructions are unpublished, so we paraphrase the definitions of Davidson et al. (2017), whose classes HateXplain adopts.

```
Hate speech expresses hatred toward a targeted social group, or uses language intended to demean, humiliate or insult people belonging to that group. Threatening or encouraging violence can qualify, but violence is not required. Offensive language is not automatically hate: interpret words in context, including everyday in-group usage and quoted lyrics, rather than judging by a word's presence alone.
```

## HateCheck

Paraphrased from the annotation guidelines and Röttger et al. (2021).

```
Hate speech is abuse directed at a protected group, or at an individual because they belong to that group. Protected characteristics include age, disability, gender reassignment and gender identity, marriage or civil partnership, pregnancy or maternity, race including colour, nationality and ethnic or national origins, religion or belief, sex and sexual orientation. Group membership must be the basis of the abuse. Abuse without a protected-group target is not hate under this definition. A slur's presence alone is insufficient: non-hateful uses, including reclaimed language or a different meaning of the same word, must be distinguished. Likewise, counterspeech and negated hate must be interpreted according to their meaning rather than the presence of hateful wording. Classify content as hateful or non-hateful.
```

## Generic definition (early experiments only)

Written for this study and supplied to every dataset in early experiments. No dataset is annotated under it, so agreement with the annotations cannot show whether models apply it correctly, and it is excluded from the paper's analysis. Its results are in `../results/generic_definition.md`.

```
Hate speech attacks a group, or a person because of group membership, on grounds of race, ethnicity, nationality, religion, gender, sexual orientation, or disability. Attacks include derogation, assertions of inferiority, dehumanization, threats or endorsement of violence, or identity-based exclusion or denial of rights. Profanity, general insults, and criticism of conduct or ideas alone are not hate. Benign identity mentions and attacks quoted, reported, discussed or rejected without author endorsement are not hate. Infer endorsement from the whole post, not a slur alone; do not invent an unclear target.
```

## References

- Davidson, T., Warmsley, D., Macy, M., and Weber, I. 2017. Automated Hate Speech Detection and the Problem of Offensive Language. ICWSM.
- Röttger, P., Vidgen, B., Nguyen, D., Waseem, Z., Margetts, H., and Pierrehumbert, J. 2021. HateCheck: Functional Tests for Hate Speech Detection Models. ACL.
- Sachdeva, P., Barreto, R., Bacon, G., Sahn, A., von Vacano, C., and Kennedy, C. 2022. The Measuring Hate Speech Corpus: Leveraging Rasch Measurement Theory for Data Perspectivism. NLPerspectives Workshop @ LREC.
- Vidgen, B., Thrush, T., Waseem, Z., and Kiela, D. 2021. Learning from the Worst: Dynamically Generated Datasets to Improve Online Hate Detection. ACL.
