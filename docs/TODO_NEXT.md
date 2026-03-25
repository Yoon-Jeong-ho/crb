# TODO NEXT

- Date: 2026-03-24

## First priority: finish CRB v2 pilot

- [ ] wait for `crb_v2_gpu2_pilot` to finish
- [ ] verify the pilot result root under `results_v2/pilot_qwen_llama_gsm8k_boolq__0434a7c315f54eec/`
- [ ] confirm per-model / per-benchmark baseline summaries exist
- [ ] confirm relation/provenance manifests exist
- [ ] confirm sweep summaries for `k=2,4` exist
- [ ] confirm aggregate files exist
- [ ] confirm incorrect pools exclude parse / format failures
- [ ] confirm dummy ordering is prefix-consistent across `k`

## Second priority: pilot bug sweep

- [ ] inspect any benchmark-specific adapter failures from the real pilot
- [ ] inspect any context overflow / truncation reason codes
- [ ] inspect any unsupported benchmark-type or parsing mismatches
- [ ] patch only the minimum issues needed for full-matrix readiness
- [ ] rerun the pilot cleanly if fixes touch baseline/pool semantics

## Third priority: full-matrix readiness decision

- [ ] verify `configs_v2/full/full_matrix.yaml`
- [ ] check GPU availability and scheduling plan
- [ ] decide whether to shard by model or benchmark family
- [ ] decide whether some 24B/32B models need separate scheduling lanes
- [ ] only launch full matrix after the pilot is clean

## Fourth priority: analysis/docs sync

- [ ] refresh current operator docs after pilot completion
- [ ] decide whether the archived legacy shareable snapshots under `docs/legacy/shareable_snapshots/` should be regenerated from v2 outputs
- [ ] add a concise v2 result summary once real pilot outputs are complete

## Do not do by default

- [ ] do not reopen legacy one-off run orchestration as the main workflow
- [ ] do not treat parse failures as incorrect dummy candidates
- [ ] do not launch the full matrix before the pilot closes cleanly


## Handoff

- `docs/HANDOFF_20260325.md`
