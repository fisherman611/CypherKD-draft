# Preliminary rule-based CypherBench error taxonomy (Qwen, seed 42)

| Method | n | Schema grounding ↓ | Graph-pattern construction ↓ | Constraint/aggregation logic ↓ | Result formulation ↓ |
|---|---:|---:|---:|---:|---:|
| Qwen3-4B (Teacher) | 2348 | 383 (16.31%) | 511 (21.76%) | 134 (5.71%) | 102 (4.34%) |
| Qwen3-0.6B (SFT) | 2348 | 1026 (43.70%) | 568 (24.19%) | 58 (2.47%) | 64 (2.73%) |
| CSD | 2348 | 671 (28.58%) | 581 (24.74%) | 98 (4.17%) | 52 (2.21%) |
| DistiLLM | 2348 | 691 (29.43%) | 562 (23.94%) | 120 (5.11%) | 32 (1.36%) |
| **CypherKD** | 2348 | 630 (26.83%) | 554 (23.59%) | 100 (4.26%) | 29 (1.24%) |

## Audit information

- A query is counted in a grouped category only when `execution_accuracy != 1` and a deterministic gold/prediction comparison detects that category.
- Categories are multi-label: one failing query may contribute to multiple columns.
- Percentages use the full test set (`n = 2348`) as denominator, matching the requested table format.
- The Teacher remains the upper bound; comparisons among student/KD systems should focus on SFT, CSD, DistiLLM, and CypherKD.
- Full case-level labels and evidence are saved in `rebuttal/full_error_taxonomy_cases_seed42.jsonl`.
- Rows with `used_in_summary: true` are the exact cases contributing to the four grouped counts; unclassified execution failures are retained for audit but do not contribute.

| Method | EX failures | Classified failures | Unclassified failures |
|---|---:|---:|---:|
| Qwen3-4B (Teacher) | 697 | 688 | 9 |
| Qwen3-0.6B (SFT) | 1158 | 1158 | 0 |
| CSD | 902 | 898 | 4 |
| DistiLLM | 888 | 881 | 7 |
| CypherKD | 831 | 828 | 3 |


## Important limitation

These labels are produced by transparent deterministic rules, not by human annotation or an LLM judge. They are suitable for a reproducible first-pass analysis and case retrieval. Before using the counts as final paper numbers, manually audit a stratified sample from every model/category and report the annotation protocol.

The [original CypherBench paper](https://aclanthology.org/2025.acl-long.438/) developed this taxonomy through manual annotation and reports an error analysis on 50 randomly sampled incorrect predictions for each of two models. It does not establish a deterministic full-test labeling procedure. Therefore, this full-test table is an extension of the original protocol and should be described as such.
