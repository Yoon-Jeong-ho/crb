# TODO NEXT

- Date: 2026-03-11

## Now

- [x] Refresh README/setup/status docs for `crb-gpu567-continuation-gpus-5`
- [x] Record that pushed baseline commits are `28e4058` and `02fa431`
- [x] Separate historical GPU4 evidence from the current GPU567 run policy
- [x] Log the first true GPU567-cycle result (`run-20260311T060823Z-1947f5cf`)

## Next runs / analysis

- [x] Inspect the 4 invalid outputs from the GPU5 parserfix smoke
- [x] Decide whether those failures are better addressed by stricter prompting or decoding, not parser regex
- [x] GPQA thinking-on parserfix follow-up smoke on **GPU 6 or 7**
- [x] One allowed multi-GPU check using only `5,6,7` (`run-20260311T061434Z-10e36149` on GPUs `5,6`)
- [x] Decide whether parserfix is good enough to keep as the active thinking-on path (`not yet`)
- [x] Run choice constrained GPQA thinking-on on GPUs `5,6` (`run-20260311T091942Z-f3e9f0fa`)
- [x] Run `/no_think` + prefill GPQA thinking-on on GPUs `5,6` (`run-20260311T092221Z-dfa04164`)
- [x] Run combined constrained + `/no_think` + prefill GPQA thinking-on on GPUs `5,6` (`run-20260311T092432Z-dac259a0`)
- [x] Compare all three against parserfix and strictfinal baselines
- [x] Pick a provisional winner (`/no_think` + prefill)

## Next decisions

- [ ] Re-run `/no_think` + prefill once more on GPUs `5,6` to check stability
- [ ] Decide whether combined config stays as fallback or gets retired
- [ ] Extend the winning control to GSM8K or MMLU
- [ ] Decide whether README / setup docs should flip the active recommendation from parserfix to `/no_think` + prefill in the next commit

## Git / reporting hygiene

- [x] Stable pushed checkpoint already exists on `origin/main`
- [x] Batch the current doc refresh with the next meaningful parserfix update
- [x] Use one short follow-up commit once parserfix direction is clearer
- [x] Report updated docs + suggested next commit message to the lead

## Do not forget

- [x] Use only `/data_x/aa007878/projects/crb/.conda/envs/crb`
- [x] Use only GPUs `5,6,7` for this continuation pass
- [x] For the 2026-03-11 evening follow-up, actually use only GPUs `5,6`
- [x] Treat GPU4 smoke results as historical carry-over evidence only
- [x] Do not call parserfix “done” while `format_failure_rate` is still `0.5`
