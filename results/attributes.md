# Attribute Classification

Macro-F1 with defined labels for Dynamic's six conduct classes (3,356 texts), HateCheck's referenced group (3,436 texts), and HateCheck's general-versus-directed hate (2,563 texts). Bold marks the highest decision-model score per task. Summarized in Appendix D of the paper.

| Model | Conduct (Dynamic) | Group (HateCheck) | Direction (HateCheck) |
|---|---:|---:|---:|
| Jev | **.538** | .989 | .682 |
| Laya | .192 | .929 | **.694** |
| Decider | .313 | .959 | .610 |
| SemIf-2B | .196 | .939 | .269 |
| SemIf-4B | .406 | .962 | .594 |
| Bespoke-Nimble | .324 | .971 | .567 |
| Luna Decisions | .535 | **.992** | .631 |
| GPT-5.6 Luna | .519 | .998 | .704 |
| DistilBERT (supervised, trained on Dynamic) | .474 | - | - |

Group and conduct tasks differ in construction and class balance, so their gap need not reflect ability. Three of Dynamic's six conduct classes each cover less than 5% of the texts.
