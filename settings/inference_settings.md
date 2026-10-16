# Inference Settings

## Local models

- Local models reject inputs that exceed their limits rather than truncating them. BART is the exception, as it truncates only the premise.
- Ties between options select the first option, so binary ties resolve to non-hate.
- Local models run on a server with an NVIDIA T4 GPU (16 GB VRAM), two Intel Xeon Gold 6230 processors (40 cores, 80 threads), and 96 GB RAM.

## Commercial LLMs (GPT-5.6 Luna, GPT-6 Sol)

- The temperature was not set, and reasoning was disabled.
- Routing was restricted to the OpenAI provider through OpenRouter, without fallbacks.
- Requests timed out after 45 seconds.
- Benchmark quality runs used four concurrent requests. The timed runs and the matched direct and decomposed runs used one.

## Luna Decisions

- Called through OpenRouter's decisions endpoint (revision 20261006, $0.10 per million input tokens).
- Its 137 refusals among 86,185 evaluation requests are excluded rather than assigned to a class. Paired comparisons for Luna Decisions use texts with valid outputs in both conditions and form separate families.
- Timed in a later serving session than the other models, and its timing includes refusals.

## Supervised classifiers

- TF-IDF with logistic regression and DistilBERT are trained on one of Dynamic, MHS, or HateXplain, and tested on all four datasets without adaptation.
- For HateXplain's three-class task, they are trained on a 5,000-post subset of the training partition and receive no definition.
