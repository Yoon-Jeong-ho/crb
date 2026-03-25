# CRB v2 Bulk Wave Operations — 2026-03-25

This note captures the bulk-first v2 launcher state as it exists in the repo on 2026-03-25.
It is limited to the bulk-wave surfaces under `results_v2/manifests/status`, `configs_v2/generated/bundles`, and `scripts_v2/`.

## 1) Bulk-first queue model

The bulk supervisor in `tools/crb_v2_bulk_supervisor.py` organizes work around four queue names.
Current operating constraint: **CRB uses GPUs 4/5/6 only; GPU7 is excluded.**

| Queue | Role | Consumed by | Notes |
| --- | --- | --- | --- |
| `main_bulk_queue` | Primary bulk queue | GPU4, GPU5 | Stable single-GPU jobs live here first. |
| `probation_queue` | Runtime-unverified queue | GPU4, GPU5, GPU6 | Used for `bulk_unverified` jobs after stable ready coverage is exhausted. |
| `retry_queue` | Retry-first queue | GPU6 | Holds retryable jobs after a failure or stale-process reconciliation. |
| `blocked` | Terminal sink | None | Used for blocked or permanently failed jobs; these rows are not scheduled. |

Current queue snapshot from `results_v2/manifests/status/queue_snapshot.json`:

- `main_bulk_queue`: 0
- `probation_queue`: 20
- `retry_queue`: 0
- `blocked`: 30

### GPU routing policy

The supervisor applies the following order when claiming jobs:

- **GPU4 / GPU5**: stable single-GPU jobs from `main_bulk_queue`, then `probation_queue` fallback
- **GPU6**: `retry_queue` first, then `probation_queue`
- **GPU7**: disabled for CRB in the current wave

## 2) Central status source of truth

The authoritative mutable state is:

- `results_v2/manifests/status/job_state.json`

The supervisor writes mirrored status views from that state:

- `results_v2/manifests/status/job_status.csv`
- `results_v2/manifests/status/job_status.json`
- `results_v2/manifests/status/queue_snapshot.json`
- `results_v2/manifests/status/workers.json`
- `results_v2/manifests/status/launched_workers.json`

### Required columns in `job_status.csv`

The supervisor writes these columns in this exact order:

1. `job_id`
2. `model`
3. `benchmark`
4. `split`
5. `condition_bundle`
6. `queue_name`
7. `priority`
8. `gpu_id`
9. `status`
10. `retry_count`
11. `failure_type`
12. `config_path`
13. `log_path`
14. `output_dir`
15. `pool_status`
16. `started_at`
17. `finished_at`
18. `next_retry_at`
19. `notes`
20. `preferred_gpu`
21. `allowed_gpus`
22. `recipe_class`

### Status values used by the supervisor

The current snapshot contains these `status` values:

- `queued`
- `running`
- `retry_wait`
- `partial_complete`
- `blocked`

The supervisor code also recognizes additional lifecycle values during reconciliation and finalization:

- `claimed`
- `failed_permanent`
- `completed`
- `skipped`

### What the current tabular snapshot shows

`results_v2/manifests/status/job_status.csv` currently has 100 rows, matching the 10 model × 10 benchmark full bundle grid.
Observed counts at the latest refresh:

- `queued`: 20
- `blocked`: 30
- `running`: 2
- `partial_complete`: 50

## 3) GPU4 / GPU5 / GPU6 / GPU7 lane roles

The supervisor starts four worker processes with these lane names:

| GPU | Lane | Role | Worker log |
| --- | --- | --- | --- |
| 4 | `main_bulk_lane_a` | Primary stable bulk lane; preferred for `qwen25_7b_instruct`, `mistral7b_instruct_v03`, and `deepseek_r1_distill_qwen_7b` when jobs are eligible for `stable_single_gpu`. | `logs/crb_v2/workers/gpu4_worker.log` |
| 5 | `main_bulk_lane_b` | Secondary stable bulk lane for the remaining `stable_single_gpu` jobs. | `logs/crb_v2/workers/gpu5_worker.log` |
| 6 | `probation_retry_lane` | Retry + probation lane; GPU7 exclusion means TP2-required jobs are blocked and GPU6 now handles retry/probation recovery. | `logs/crb_v2/workers/gpu6_worker_restarted.log` |
| 7 | `disabled` | Not used by CRB in the current wave. | N/A |

### Launch snapshot

The launch snapshot recorded in `results_v2/manifests/status/launched_workers.json` is:

| GPU | PID | Lane | Log path |
| --- | ---: | --- | --- |
| 4 | 2888057 | `main_bulk_lane_a` | `logs/crb_v2/workers/gpu4_worker_restarted.log` |
| 5 | 2888058 | `main_bulk_lane_b` | `logs/crb_v2/workers/gpu5_worker_restarted.log` |
| 6 | 2884107 | `probation_retry_lane` | `logs/crb_v2/workers/gpu6_worker_restarted.log` |
| 7 | disabled | `disabled` | N/A |

`results_v2/manifests/status/workers.json` is the current live worker-state view.

## 4) Commands

These command paths are present in the repo and were verified against the script contents before this note was written.

### Refresh inventory / bundle manifests

```bash
scripts_v2/refresh_v2_inventory.sh
```

- Wrapper around `tools/crb_v2_prepare_wave.py`
- Regenerates analysis tables, queue manifests, and generated bundle YAMLs
- Also recreates the `logs/crb_v2/gpu4` through `logs/crb_v2/gpu7` directories

### Start the bulk wave

```bash
scripts_v2/start_bulk_wave.sh
```

- Refuses to start if a `tools/crb_v2_bulk_supervisor.py worker` process is already running
- Runs the supervisor with `start`, which initializes state and launches the four workers

### Resume bulk workers

```bash
scripts_v2/resume_bulk_workers.sh
```

- Uses the same duplicate-launch guard as `start_bulk_wave.sh`
- Runs the supervisor with `launch-workers` so it can restart workers from an existing state file

### Show bulk status

```bash
scripts_v2/bulk_status.sh
```

- Prints `results_v2/manifests/status/workers.json`
- Prints `results_v2/manifests/status/queue_snapshot.json`
- Prints `results_v2/summary/bulk_coverage_summary.json`
- Lists the top active jobs from `results_v2/manifests/status/job_status.csv`

## 5) Generated bundle configs

`configs_v2/generated/bundles/` is the generated bundle root.
It currently contains 100 YAML files: 10 model directories × 10 benchmark configs each.

### Model directories present

- `deepseek_r1_distill_llama_8b`
- `deepseek_r1_distill_qwen_7b`
- `gemma2_9b_it`
- `llama31_8b_instruct`
- `mistral7b_instruct_v03`
- `mistral_small_24b_instruct_2501`
- `olmo2_1124_7b_instruct`
- `phi4_mini_instruct`
- `qwen25_7b_instruct`
- `qwq_32b`

### Path pattern

Each generated bundle uses this layout:

```text
configs_v2/generated/bundles/<model>/<benchmark>.yaml
```

Examples already in the tree include:

- `configs_v2/generated/bundles/qwen25_7b_instruct/gsm8k.yaml`
- `configs_v2/generated/bundles/llama31_8b_instruct/gpqa.yaml`
- `configs_v2/generated/bundles/olmo2_1124_7b_instruct/truthfulqa_mc.yaml`

## 6) Operational notes

- `job_status.csv` and `job_status.json` are the easiest files to read for queue health.
- `job_state.json` is the file the supervisor mutates under lock.
- `queue_snapshot.json` is the quickest summary of queue depth.
- `workers.json` is the live worker-state view.
- Job-level logs are written under `logs/crb_v2/jobs/gpu*/`, while worker logs are written under `logs/crb_v2/workers/`.
- Current remaining live work is concentrated in the runtime-unverified probation set:
  - `deepseek_r1_distill_llama_8b`
  - `olmo2_1124_7b_instruct`
- Current blocked set includes:
  - `gemma2_9b_it`
  - `mistral_small_24b_instruct_2501`
  - `qwq_32b`
