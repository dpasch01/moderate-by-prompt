# Luna Decisions Coverage

Luna Decisions occasionally refuses a request. Refusals are excluded rather than assigned to a class. Paired comparisons for Luna Decisions use texts with valid outputs in both conditions and form separate correction families.

Across test conditions, there are 135 refusals among 85,585 requests. Including the 600 validation requests for threshold tuning, there are 137 refusals among 86,185 requests. Counts are requests across conditions, not unique texts.

## Requests by condition

| Dataset | Condition | Requested | Valid | Refused |
|---|---|---:|---:|---:|
| Dynamic | Benchmark direct | 4,120 | 4,111 | 9 |
| MHS | Benchmark direct | 3,203 | 3,203 | 0 |
| HateXplain | Benchmark direct | 1,924 | 1,924 | 0 |
| HateCheck | Benchmark direct | 3,728 | 3,719 | 9 |
| HateXplain | Three-class | 1,924 | 1,924 | 0 |
| Dynamic | No definition | 4,120 | 4,120 | 0 |
| MHS | No definition | 3,203 | 3,203 | 0 |
| HateXplain | No definition | 1,924 | 1,924 | 0 |
| HateCheck | No definition | 3,728 | 3,728 | 0 |
| Dynamic | Matched direct (A) | 4,120 | 4,098 | 22 |
| MHS | Matched direct (A) | 3,203 | 3,203 | 0 |
| HateXplain | Matched direct (A) | 1,924 | 1,924 | 0 |
| HateCheck | Matched direct (A) | 3,728 | 3,719 | 9 |
| Dynamic | Decomposed (B) | 4,120 | 4,118 | 2 |
| MHS | Decomposed (B) | 3,203 | 3,203 | 0 |
| HateXplain | Decomposed (B) | 1,924 | 1,924 | 0 |
| HateCheck | Decomposed (B) | 3,728 | 3,728 | 0 |
| Dynamic | Conduct type, defined | 3,356 | 3,352 | 4 |
| Dynamic | Conduct type, no definition | 3,356 | 3,356 | 0 |
| HateCheck | Referenced group, defined | 3,436 | 3,410 | 26 |
| HateCheck | Referenced group, no definition | 3,436 | 3,390 | 46 |
| HateCheck | Direction, defined | 2,563 | 2,557 | 6 |
| HateCheck | Direction, no definition | 2,563 | 2,563 | 0 |
| Dynamic | Threshold tuning (validation) | 200 | 199 | 1 |
| MHS | Threshold tuning (validation) | 200 | 200 | 0 |
| HateXplain | Threshold tuning (validation) | 200 | 199 | 1 |
| Dynamic | Generic definition | 4,120 | 4,119 | 1 |
| MHS | Generic definition | 3,203 | 3,203 | 0 |
| HateCheck | Generic definition | 3,728 | 3,727 | 1 |
| HateXplain | Generic definition | 1,000 | 1,000 | 0 |
| HateXplain | Generic definition, three-class | 1,000 | 1,000 | 0 |

The generic-definition condition on HateXplain uses an earlier 1,000-text cohort.

## Paired valid texts

| Dataset | Comparison | Paired valid N |
|---|---|---:|
| Dynamic | No definition vs Benchmark direct | 4,111 |
| Dynamic | Matched direct (A) vs Decomposed (B) | 4,098 |
| Dynamic | Benchmark direct vs Matched direct (A) | 4,095 |
| Dynamic | Benchmark direct vs Decomposed (B) | 4,111 |
| Dynamic | Generic definition vs Benchmark direct | 4,111 |
| MHS | No definition vs Benchmark direct | 3,203 |
| MHS | Matched direct (A) vs Decomposed (B) | 3,203 |
| MHS | Benchmark direct vs Matched direct (A) | 3,203 |
| MHS | Benchmark direct vs Decomposed (B) | 3,203 |
| MHS | Generic definition vs Benchmark direct | 3,203 |
| HateXplain | No definition vs Benchmark direct | 1,924 |
| HateXplain | Matched direct (A) vs Decomposed (B) | 1,924 |
| HateXplain | Benchmark direct vs Matched direct (A) | 1,924 |
| HateXplain | Benchmark direct vs Decomposed (B) | 1,924 |
| HateXplain | Generic definition vs Benchmark direct | 1,000 |
| HateCheck | No definition vs Benchmark direct | 3,719 |
| HateCheck | Matched direct (A) vs Decomposed (B) | 3,719 |
| HateCheck | Benchmark direct vs Matched direct (A) | 3,712 |
| HateCheck | Benchmark direct vs Decomposed (B) | 3,719 |
| HateCheck | Generic definition vs Benchmark direct | 3,718 |
