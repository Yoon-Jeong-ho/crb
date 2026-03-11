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

## Git / reporting hygiene

- [x] Stable pushed checkpoint already exists on `origin/main`
- [x] Batch the current doc refresh with the next meaningful parserfix update
- [x] Use one short follow-up commit once parserfix direction is clearer
- [x] Report updated docs + suggested next commit message to the lead

## Do not forget

- [x] Use only `/data_x/aa007878/projects/crb/.conda/envs/crb`
- [x] Use only GPUs `5,6,7` for this continuation pass
- [x] Treat GPU4 smoke results as historical carry-over evidence only
- [x] Do not call parserfix “done” while `format_failure_rate` is still `0.5`
