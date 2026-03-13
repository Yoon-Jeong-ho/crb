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
8. **The GPU5/6 follow-up sweep proved that final-answer control can remove invalids entirely.**
   - `run-20260311T092221Z-dfa04164` and `run-20260311T092432Z-dac259a0` both achieved `format_failure = 0.0` with `parsed_count = 8/8`.
9. **Choice-only constrained decoding is not a safe default by itself.**
   - `run-20260311T091942Z-f3e9f0fa` removed parse failures,
   - but accuracy fell to `0.25` because the output effectively collapsed to all `A`.
10. **`/no_think` + prefill is the current best tradeoff.**
   - It kept accuracy at `0.375` (matching the parserfix baseline),
   - while removing the baseline’s `4/8` invalid outputs.

## What this result means

- The branch is no longer only a docs/planning hypothesis.
- The old parserfix-only path is still informative, but it is no longer the best active lane.
- The better interpretation now is:
  - **parserfix** showed the branch could run,
  - **strict-final** showed that stronger formatting pressure hurts accuracy,
  - **`/no_think` + prefill** showed that target-turn control can remove invalids without losing the parserfix-level accuracy.
- In other words, the main blocker moved from “can we get a clean final answer at all?” to **“which clean-output control should become the default?”**
- Combined constrained + `/no_think` + prefill is viable, but it did not beat the simpler `/no_think` + prefill variant on accuracy.

## Practical next step

- Highest-value next action now: treat **`/no_think` + prefill** as the provisional winner and rerun/extend it before adding new control complexity.
- Multi-GPU verification is already done for the allowed set, so the next action should be **replication or dataset extension**, not infra work.

## External documentation research summary

- Qwen 공식 문서는 thinking mode에서 `temperature=0.6`, `top_p=0.95`, `top_k=20`을 권장한다.
- 같은 문서에서 `/think`, `/no_think`, assistant prefill `<think>\n\n</think>\n\n` 로 turn-level 제어가 가능하다고 안내한다.
- vLLM 공식 문서는 structured outputs `choice` / `regex` 제약을 지원한다.
- 현재 결과와 합치면, 가장 유망한 개선 방향은:
  1. parser 추가보다 **target turn thinking control**
  2. `/no_think` + prefill 경로의 재현 및 다른 dataset 확장
  3. choice-only constraint는 active default로 쓰지 않기
