# Model Revisions and Inference Settings

Hash prefixes identify the pinned checkpoints. Hosted identifiers do not guarantee unchanged weights. A machine-readable version is in `models.csv`.

| Model | Checkpoint or identifier | Precision | Input limit | Decision |
|---|---|---|---|---|
| Jev | `jev-1.13.0` (hosted API) | - | - | Choice question, option scores |
| Laya | `1c5edc17` | FP32, BF16 autocast | 1,024 tokens (2,048 for B) | Option scores with the released temperature scaling |
| Decider | `b37f7e1b` | BF16 | 512 tokens | Option-letter scores, scoring temperature 1.3 |
| SemIf-2B | Qwen `15852e8c`, SemIf `ca3ba65f` | BF16 | 4,096 tokens | Next-letter probabilities |
| SemIf-4B | Qwen `851bf6e8`, SemIf `ca3ba65f` | BF16 | 4,096 tokens | Next-letter probabilities |
| Bespoke-Nimble | adapter `594dfdcf`, Qwen3.5-9B `c2022362` | NF4, BF16 compute | 2,048 tokens | Letter-code probabilities |
| Luna Decisions | `openai/gpt-6-luna-decisions-20261006` | - | - | OpenRouter decisions endpoint, option scores |
| CoPE-A-9B | adapter `0d95d1e2`, Gemma-2-9B `33c19302` | NF4, BF16 compute | 8,191 tokens | Greedy one-token 0/1 answer |
| BART-large-MNLI | `d7645e12` | FP32, BF16 autocast | 1,024 tokens | Entailment softmax across candidates |
| GPT-5.6 Luna | `openrouter/openai/gpt-5.6-luna` | - | - | Strict JSON, reasoning off, max. 64 tokens |
| GPT-6 Sol | `openrouter/openai/gpt-6-sol` | - | - | Strict JSON, reasoning off, max. 64 tokens |
| DistilBERT | `12040acc` | - | - | Fine-tuned classifier |
