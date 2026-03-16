# CONTINUATION AUDIT — 2026-03-16

## Scope
- Audit target repo: `/data_x/aa007878/projects/crb`
- Audit inspection cwd: `/data_x/aa007878/projects/crb`
- Authoritative execution cwd for CRB runs: `/data_x/aa007878/projects/crb/Legacy`
- Authoritative conda env for CRB runs: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- Artifact roots:
  - runs: `/data_x/aa007878/projects/crb/Legacy/results/runs`
  - manifests: `/data_x/aa007878/projects/crb/Legacy/results/manifests`
  - logs: `/data_x/aa007878/projects/crb/Legacy/logs`
  - scoreboard: `/data_x/aa007878/projects/crb/Legacy/results/summary/scoreboard.csv`
- Audit rule: inspect only; do **not** launch experiments.

## Repository state at audit time
- Branch: `main`
- Dirty artifact state was present at audit time:
  - modified: `/data_x/aa007878/projects/crb/Legacy/results/summary/scoreboard.csv`
  - untracked manifests:
    - `/data_x/aa007878/projects/crb/Legacy/results/manifests/qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4__manifest__06dfa480636004d0.json`
    - `/data_x/aa007878/projects/crb/Legacy/results/manifests/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k4__manifest__06dfa480636004d0.json`
    - `/data_x/aa007878/projects/crb/Legacy/results/manifests/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8__manifest__06dfa480636004d0.json`

## Why `Legacy/` is still the authoritative runnable path
The root repo is still a bootstrap/documentation wrapper, not an independent runnable CRB tree.

Concrete evidence:
- `/data_x/aa007878/projects/crb/src/crb -> /data_x/aa007878/projects/crb/Legacy/src/crb`
- `/data_x/aa007878/projects/crb/tests -> /data_x/aa007878/projects/crb/Legacy/tests`
- `/data_x/aa007878/projects/crb/configs -> /data_x/aa007878/projects/crb/Legacy/configs`
- `/data_x/aa007878/projects/crb/scripts -> /data_x/aa007878/projects/crb/Legacy/scripts`
- `/data_x/aa007878/projects/crb/data -> /data_x/aa007878/projects/crb/Legacy/data`
- `/data_x/aa007878/projects/crb/README.md` and `/data_x/aa007878/projects/crb/CRB_EXPERIMENT_SETUP.md` both say to execute from `Legacy/` with `PYTHONPATH=src`.
- `/data_x/aa007878/projects/crb/docs/PIPELINE_STATUS.md` records the chosen bridge strategy as wrap/symlink, not promote/delete.

Operational conclusion:
- For runnable configs, tests, generated manifests, logs, and results, treat `/data_x/aa007878/projects/crb/Legacy` as source of truth.
- Treat `/data_x/aa007878/projects/crb` as the coordination/docs root.

## Current experiment status from docs + on-disk artifacts
### Documented baseline already established before this audit
The 2026-03-11 docs already establish:
- `/data_x/aa007878/projects/crb/README.md`
- `/data_x/aa007878/projects/crb/docs/EXECUTION_STATUS.md`
- `/data_x/aa007878/projects/crb/docs/RESULTS_LOG.md`
- `/data_x/aa007878/projects/crb/docs/ANALYSIS.md`

Those docs agree that:
- the GPU567 continuation pass made `Legacy/` the active runnable lane,
- `/no_think` + prefill became the best documented GPQA thinking-on rescue path,
- root-level bridge files are wrappers around `Legacy/`.

### Newer completed artifacts visible during this audit
`/data_x/aa007878/projects/crb/Legacy/results/summary/scoreboard.csv` contains three newer GSM8K scoreboard rows beyond the 2026-03-11 docs:
- canonical baseline (`k=0`):
  - run id: `run-20260315T165946Z-4c205a03`
  - JSON: `/data_x/aa007878/projects/crb/Legacy/results/runs/qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k0__4c205a0348faf24c/run-20260315T165946Z-4c205a03.json`
  - accuracy: `0.6353297952994693`
  - format failure rate: `0.0576194086429113`
- wrong-history cross-domain (`k=2`):
  - run id: `run-20260315T183659Z-249600c4`
  - JSON: `/data_x/aa007878/projects/crb/Legacy/results/runs/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k2__249600c495a1b11a/run-20260315T183659Z-249600c4.json`
  - accuracy: `0.3813495072024261`
  - format failure rate: `0.1106899166034875`
- wrong-history cross-domain (`k=4`):
  - run id: `run-20260315T231541Z-3515c4d1`
  - JSON: `/data_x/aa007878/projects/crb/Legacy/results/runs/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k4__3515c4d1912c731d/run-20260315T231541Z-3515c4d1.json`
  - accuracy: `0.36770280515542075`
  - format failure rate: `0.04169825625473844`

These rows mean the repo has moved beyond the 2026-03-11 GPQA-only continuation snapshot and is now partway through a GSM8K protocol/wrong-history sweep.

### Incomplete sweep state visible on disk
Two later GSM8K runs were left incomplete at audit time.

1. Canonical `k=4`
- config: `/data_x/aa007878/projects/crb/Legacy/configs/generated/qwen3_protocol_k_sweep_full/qwen3_gsm8k_on_canonical__k-4.yaml`
- manifest: `/data_x/aa007878/projects/crb/Legacy/results/manifests/qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4__manifest__06dfa480636004d0.json`
- log: `/data_x/aa007878/projects/crb/Legacy/logs/qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4__4aaef99e42f6b549.log`
- partial dir: `/data_x/aa007878/projects/crb/Legacy/results/runs/qwen3_1p7b_gsm8k_protocol_kfull_gsm8k_on_canonical_k4__4aaef99e42f6b549`
- observed state: `partial_results.jsonl` exists with `569` lines, but there is no final `run-*.json` and no scoreboard row.

2. Wrong-history cross-domain `k=8`
- config: `/data_x/aa007878/projects/crb/Legacy/configs/generated/qwen3_wrong_history_full/gsm8k_wrong_history_cross_domain__k-8.yaml`
- manifest: `/data_x/aa007878/projects/crb/Legacy/results/manifests/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8__manifest__06dfa480636004d0.json`
- log: `/data_x/aa007878/projects/crb/Legacy/logs/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8__0290e6d4dc431126.log`
- partial dir: `/data_x/aa007878/projects/crb/Legacy/results/runs/qwen3_1p7b_gsm8k_gsm8k_wrong_history_cross_domain_full_k8__0290e6d4dc431126`
- observed state: `partial_results.jsonl` exists with `48` lines, but there is no final `run-*.json` and no scoreboard row.

Additional audit observation:
- no active `crb.cli.run_eval` process was visible during the audit, so these look like interrupted or abandoned partial runs, not currently executing jobs.

## Next runnable sweep recommendation
Do **not** widen scope yet. Finish the interrupted GSM8K sweep first.

Recommended next runnable sweep:
1. re-run or resume `/data_x/aa007878/projects/crb/Legacy/configs/generated/qwen3_protocol_k_sweep_full/qwen3_gsm8k_on_canonical__k-4.yaml`
2. re-run or resume `/data_x/aa007878/projects/crb/Legacy/configs/generated/qwen3_wrong_history_full/gsm8k_wrong_history_cross_domain__k-8.yaml`
3. then run `/data_x/aa007878/projects/crb/Legacy/configs/generated/qwen3_protocol_k_sweep_full/qwen3_gsm8k_on_canonical__k-8.yaml`

Rationale:
- the repo already has completed GSM8K anchors for canonical `k=0` and wrong-history `k=2,4`;
- the most urgent gap is incomplete artifact closure, not new dataset expansion;
- once canonical `k=4,8` and wrong-history `k=8` are complete, the GSM8K lane will finally support a clean `k`-sweep comparison instead of a mixed completed/partial state.

## GPU 4/5/6/7 planning note
- Planning availability now includes GPUs `4,5,6,7`.
- However, the currently documented continuation policy in `/data_x/aa007878/projects/crb/README.md` and `/data_x/aa007878/projects/crb/CRB_EXPERIMENT_SETUP.md` still treats `5,6,7` as the continuation launch set and GPU4 as historical/baseline material.
- Therefore the safest plan is:
  - prefer GPUs `5,6,7` for the next runnable sweep,
  - keep GPU4 as an overflow option only if the team explicitly decides to relax the earlier continuation policy.

## Concrete acceptance checks for the next sweep
A run should count as complete only if **all** of the following are true.

### Artifact-completion checks
- A manifest exists under `/data_x/aa007878/projects/crb/Legacy/results/manifests/` for the exact config/run lane.
- A final run JSON exists under `/data_x/aa007878/projects/crb/Legacy/results/runs/<run_dir>/run-*.json`.
- A log exists under `/data_x/aa007878/projects/crb/Legacy/logs/` and reaches normal end-of-run summary output.
- `/data_x/aa007878/projects/crb/Legacy/results/summary/scoreboard.csv` has a matching row for the final run id.
- No lane is left in a partial-only state (`partial_results.jsonl` without final JSON + scoreboard row).

### Consistency checks
- `run_id`, `k`, `dataset`, `history_mode`, and `thinking_mode` must agree across config name, log name, run JSON, and scoreboard row.
- `num_total` in the run JSON must equal the line count in `partial_results.jsonl` at completion.
- For GSM8K full-sample runs, `num_total` should close at `1319`, not a truncated partial count.

### Comparison checks
- Update the GSM8K comparison table after completion so it includes:
  - canonical `k=0,4,8`
  - wrong-history cross-domain `k=2,4,8`
- Compare at minimum:
  - accuracy trend across `k`
  - format failure trend across `k`
  - whether wrong-history remains materially worse than canonical once the interrupted lanes are completed.

## Audit takeaway
- `Legacy/` remains the only authoritative runnable CRB path.
- The repo is mid-sweep, not cleanly finished: three newer GSM8K rows are completed, but two later GSM8K lanes are stranded in partial-only state.
- The next practical step is to close the interrupted GSM8K sweep before adding new datasets or new control variants.
