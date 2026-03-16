# Related Work Buckets

Use these buckets when drafting the CRB framing or deciding which comparisons to foreground.

## 1. Benchmark foundations

- MMLU
- GSM8K
- GPQA
- AIME

These justify the underlying target tasks before CRB changes the evaluation protocol.

## 2. Long-context robustness

- Lost in the Middle
- LongBench
- Same Task, More Tokens
- RULER
- BABILong
- Summary of a Haystack

These are the closest comparisons for context-length and retrieval-style failure modes, but they do not isolate target-only interference the way CRB does.

## 3. Multi-turn chat evaluation

- MT-Bench / LLM-as-a-Judge

CRB also uses multi-turn structure, but its scoring objective differs: earlier turns are interference and only the final target answer is scored.

## 4. Reasoning-control / output-control work

- prompt-based answer-format control
- constrained decoding / structured output control
- thinking-mode control (`/think`, `/no_think`, prefill)

This bucket supports the interpretation that some failures are output-surface failures rather than pure reasoning failures.
