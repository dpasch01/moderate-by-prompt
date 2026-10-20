# Inference Settings

## Local models

- Local models reject inputs that exceed their limits rather than truncating them. BART is the exception, as it truncates only the premise.
- Ties between options select the first option, so binary ties resolve to non-hate.
- Local models run on one NVIDIA GeForce RTX 5070 Ti GPU (16 GB), with an AMD Ryzen 9 5950X processor (16 cores, 32 threads) and 32 GB RAM, using torch 2.11 with CUDA 12.8.

## Commercial LLMs (GPT-5.6 Luna, GPT-6 Sol)

- The temperature was not set, and reasoning was disabled.
- Routing was restricted to the OpenAI provider through OpenRouter, without fallbacks.
- Requests timed out after 45 seconds.
- Benchmark quality runs used four concurrent requests. The timed runs and the matched direct and decomposed runs used one.

## Luna Decisions

- Called through OpenRouter's decisions endpoint (revision 20261006, $0.10 per million input tokens).
- Its 135 refusals among 85,585 test-condition requests are excluded rather than assigned to a class. Counting the 600 development requests for threshold tuning, there are 137 refusals among 86,185 requests. Per-condition coverage is in `../results/luna_decisions_coverage.md`. Paired comparisons for Luna Decisions use texts with valid outputs in both conditions and form separate families.
- Timed in a later serving session than the other models, and its timing includes refusals.

## Supervised classifiers

- TF-IDF with logistic regression and DistilBERT are trained on one of Dynamic, MHS, or HateXplain, and tested on all four datasets without adaptation. They receive no definition.
- **TF-IDF+LR:** union of word 1–2 grams (50,000 maximum features) and character 3–5 grams (100,000 maximum features), each with min_df 2 and sublinear term frequency. Logistic regression with max_iter 1,000 and random_state 42, otherwise library defaults (L2, lbfgs), no class weighting. C is selected from 0.1, 1, and 10 by source-validation macro-F1 (first value on ties). Selected C: Dynamic 1, MHS 10, HateXplain 10.
- **DistilBERT:** `distilbert-base-uncased` (revision `12040accade4e8a0f71eabdb258fecc2e7e948be`), AdamW with learning rate 2e-5 and weight decay 0.01, batch size 32, first 256 tokens, three epochs, seed 42. The epoch with the highest source-validation macro-F1 is kept (earliest on ties). Selected epochs: Dynamic 3, MHS 2, HateXplain 2.
- For HateXplain's three-class task, both are trained on a 5,000-post subset of the training partition with the same settings (TF-IDF C = 1).
- Training data serve only the supervised baselines. Validation data also select the tuned thresholds (A*) and the cascade referral rates.
