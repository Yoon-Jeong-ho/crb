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
6. **GPU6 strict-final follow-up clarified the tradeoff.**
   - `run-20260311T063838Z-7956de92` improved format failure (`0.5 -> 0.375`)
   - but degraded accuracy (`0.375 -> 0.125`)
   - so stricter final-answer prompting alone is not the full fix.
7. **AIME numeric path is still alive on the allowed GPU set.**
   - `run-20260311T064335Z-1ab1abe2` on GPU `7` reproduced the same general AIME quality band (`accuracy 0.125`, `format_failure 0.25`).

## What this result means

- The branch is no longer only a docs/planning hypothesis.
- The branch is also not yet “fixed”: half of the items still failed format/parsing.
- So the right interpretation is **partial validation, not closure**.
- The invalid outputs we inspected end mid-reasoning and lack a final `Answer: <letter>` line.
- That makes the next fix target more specific: **final-answer emission / truncation control**, not just parser regex expansion.
- The GPU6 strict-final rerun confirms that “force a stricter final answer” can improve parseability but still damage answer quality.
- Therefore the next step should target **gentler final-answer control or decoding changes**, not simply stronger formatting pressure.

## Practical next step

- Highest-value next action after these reruns: choose one follow-up thinking-on config that improves final-answer emission without sacrificing too much accuracy.
- Multi-GPU verification is already done for the allowed set, so the next config change should target **final-answer emission**, not infrastructure.
