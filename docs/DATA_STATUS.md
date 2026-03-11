# DATA STATUS

- Date: 2026-03-11
- Scope priority: `gpqa`, `gsm8k`, `aime`, `mmlu-family`

## Dataset readiness snapshot
- [x] GPQA — adapter/path/schema re-verified via fresh GPU4 smoke (`run-20260311T054045Z-c4316b30`)
- [x] GSM8K — adapter/path/schema re-verified via fresh offline dataset load on 2026-03-11
- [x] AIME — numeric parse/eval path re-verified in active root and fresh GPU7 offline smoke (`run-20260311T064335Z-1ab1abe2`)
- [x] MMLU-family — adapter/path/schema re-verified via fresh offline dataset load on 2026-03-11

## Normalized common format
- `dataset_name`
- `split`
- `item_id`
- `domain`
- `subject`
- `question`
- `choices`
- `answer`
- `answer_type`

## Known from docs / Legacy
- GPQA
  - adapter: `gpqa`
  - answer_type: `mcq`
  - subject source: `Subdomain`
  - domain source: `High-level domain`
  - fresh smoke evidence: `Legacy/results/runs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off_gpu4_worker5_smoke_20260311__c4316b30556d7ecf/run-20260311T054045Z-c4316b30.json`
- GSM8K
  - adapter: `gsm8k`
  - answer_type: `numeric`
  - normalized domain/subject: `math` / `arithmetic`
- AIME
  - adapter: `aime`
  - answer_type: `numeric`
  - normalized domain/subject: `math` / `aime`
  - `cross_domain` needs cross-dataset dummy support in practice
- MMLU-family
  - adapter: `mmlu`
  - answer_type: `mcq`
  - subject/domain normalization handled in loader heuristics

## To confirm
- [x] Internal common fields confirmed in `Legacy/src/crb/datasets/hf_loaders.py`
- [x] `same_domain` policy = same normalized `subject` or broad `domain`
- [x] `cross_domain` policy = different normalized `subject` and broad `domain`
- [x] Manifest generation / reuse path exists in `Legacy/src/crb/sampling/dummy_sampler.py`
- [x] Fresh cache/access check for GSM8K and MMLU on this machine
- [x] Fresh AIME numeric rerun in the current bootstrap path

## Risks
- AIME `cross_domain` is weak if dummy pool stays math-only.
- Real-dataset reruns may still need unsandboxed HF access on a cold cache.
- Offline local-model runs currently record the snapshot path in `model_name`; normalize later if needed.
