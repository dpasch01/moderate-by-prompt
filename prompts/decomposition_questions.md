# Decomposition Questions and Rules

We derived all component questions, answer descriptions, and rules from the dataset documentation and froze them before evaluation. They are our operationalizations, not rules published by the dataset authors.

In decomposed classification (B), each model answers the component questions, and the fixed rule below combines the answers into the verdict. The questions and answer descriptions also form the policy glossary that both direct (A) and decomposed (B) classification receive (see `instructions.md`).

## Dynamic

**Rule:** Hate if `intentional` is yes and either `conduct` is support, or `scope` is yes and `conduct` is animosity, derogation, dehumanization, or threatening. Otherwise non-hate. The support route follows the codebook's exception to requiring an identifiable victim.

```
[scope] Is the expression aimed at people because of an identity within this policy scope?
  no: No such identity-directed target is conveyed. A named hateful entity alone need not identify its victims.
  yes: People are targeted because of a vulnerable, marginalized or discriminated-against group identity. The identity may be implied. Scope is open-ended; men, white people and heterosexuals as such are excluded.

[intentional] Does the text convey intentional expression of the negative conduct or support, rather than merely report or reject it?
  no: The text does not convey such intent, including mere reporting or rejection, a mistake, or ignorance without intentional negative expression.
  yes: The text conveys intentional negative expression or support. Infer communicative intent from the text; an explicit confession of intent is not required.

[conduct] Which single category best describes the expressed conduct? Assess conduct separately from the scope and intent gates.
  none: None of these forms of negative conduct or support is conveyed.
  animosity: Implicit or subtle negative treatment of a group.
  derogation: Explicit group-directed contempt, demonization, inferiority, insult or intensely negative feeling.
  dehumanization: Explicitly negative, malicious portrayal of a group as less than human; a benign animal comparison is insufficient.
  threatening: Expression, desire, encouragement, justification or celebration of action causing serious OR imminent harm to a group; both action and harm are required.
  support: Glorification, endorsement or encouragement of support for unambiguously hateful entities, or denial of established identity-based atrocities. Victims need not be named; mere sharing without positive support is insufficient.
```

## MHS

**Rule:** Hate if `targeting` and `abuse` are both yes. Otherwise non-hate. Unnecessary labeling, emphasized by the definition, is not required.

```
[targeting] Is the language directed at a person or group because of actual or perceived innate characteristics?
  no: No such characteristic-based direction is conveyed.
  yes: The language is directed at someone on the basis of actual or perceived innate characteristics.

[abuse] Does the expression convey prejudice-driven hostile or malicious language?
  no: Neither prejudice-driven hostility nor malice is conveyed.
  yes: Prejudice-driven hostility OR malice is conveyed.
```

## HateXplain

**Rule:** Hate if `targeting` and `abuse` are both yes. Otherwise non-hate, with offensive and normal posts both mapping to non-hate.

```
[targeting] Is a social group, or people as members of that group, the target of the expression?
  no: No group-directed target is conveyed; a mention alone is not targeting.
  yes: A social group or people as members of that group are targeted, explicitly or implicitly.

[abuse] In context, does the expression convey group hatred or intended demeaning, humiliation or insult toward people belonging to the group?
  no: No such meaning is conveyed. Offensive words alone are insufficient; interpret everyday in-group usage and quoted lyrics in context rather than automatically counting or exempting them.
  yes: It expresses group hatred OR intends to demean, humiliate or insult people as group members. Group-directed threats or encouragement of violence can qualify; violence is not necessary.
```

## HateCheck

**Rule:** Hate if `targeting` and `abuse` are both yes for the same target. Otherwise non-hate.

```
[targeting] Is a protected group, or a person because of their membership in that group, the target of the expression?
  no: No such protected-group-based targeting is conveyed. Mention of an identity alone is insufficient; objects, professions and personal attacks unrelated to protected membership do not qualify.
  yes: The expression targets a group or a person on the basis of a protected characteristic listed in the policy, explicitly or through context. Evaluate targeting separately from whether the expression is abusive.

[abuse] Does the expression, interpreted in its full context, convey abuse toward the target under consideration?
  no: The expression does not convey abuse toward that target in context. Mere identity mention, a different meaning of a slur, non-abusive reclaimed usage, rejection of abuse and genuinely negated abuse are insufficient.
  yes: The expression conveys abuse toward that target. Interpret the meaning in context rather than merely detecting a word. A question, opinion, negation or quotation is not automatically exempt if the resulting expression remains abusive.
```
