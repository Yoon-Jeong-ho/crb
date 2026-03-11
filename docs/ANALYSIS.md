# ANALYSIS

- Date: 2026-03-11

## Current conclusions

1. **`Legacy/` is still the only runnable CRB tree.**
   - Root remains documentation/bootstrap glue.
   - Therefore all new technical validation still depends on `Legacy/` execution.
2. **The pushed baseline is already established.**
   - `28e4058` and `02fa431` are on `origin/main`.
   - Those commits define the current stable documentation checkpoint.
3. **This continuation pass still uses GPUs `5,6,7 only`.**
   - Earlier same-day GPU4 smoke evidence remains useful reference, but it is carry-over evidence for this pass.
4. **The parserfix branch has now crossed the “first successful run” gate.**
   - `run-20260311T060823Z-1947f5cf` proves the GPU567 branch can produce a fresh GPQA thinking-on result.
   - But `format_failure_rate = 0.5` and `invalid_count = 4` show that parser/final-answer handling is still the main bottleneck.
5. **The allowed-set multi-GPU path is also re-verified.**
   - `run-20260311T061434Z-10e36149` on GPUs `5,6` succeeded cleanly.
   - So the remaining blocker is not multi-GPU execution stability; it is thinking-on final-answer quality.

## What this result means

- The branch is no longer only a docs/planning hypothesis.
- The branch is also not yet “fixed”: half of the items still failed format/parsing.
- So the right interpretation is **partial validation, not closure**.
- The invalid outputs we inspected end mid-reasoning and lack a final `Answer: <letter>` line.
- That makes the next fix target more specific: **final-answer emission / truncation control**, not just parser regex expansion.

## Practical next step

- Highest-value next action: inspect the 4 invalid outputs from `run-20260311T060823Z-1947f5cf`.
- After that, rerun once on GPU 6 or 7 to check whether the partial improvement is stable.
- Multi-GPU verification is already done for the allowed set, so the next config change should target **final-answer emission**, not infrastructure.
