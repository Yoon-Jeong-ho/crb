# CRB: Conversation-Accumulated / Multi-Turn Interference Benchmark

CRB is a reproducible experiment pipeline for measuring how a model's answer to a **final target problem** changes after accumulating **dummy question-answer turns** in its prior conversation history.

The benchmark supports:
- **multi-turn accumulated evaluation**
- **single-turn flattened control**
- **self-history vs oracle-history**
- **same-domain vs cross-domain dummy histories**
- **k-shot dummy history sweeps**
- **run-level JSON outputs**
- **cumulative CSV scoreboard logging**
- **reusable, model-independent evaluation pack manifests**

The implementation uses the **vLLM Python API** as the primary inference backend so the same codepath can be used for single-GPU and multi-GPU runs with config-only changes.

---

## 1. Experiment definition

For each target benchmark item:
1. Select a fixed, reproducible **dummy pack**.
2. Insert `k` dummy turns before the final target question.
3. Score **only the final target answer**.
4. Compare accuracy across:
   - `multi_turn`
   - `single_turn_flattened`
   - `self_history`
   - `oracle_history`
   - `same_domain`
   - `cross_domain`
   - multiple `k` values

### Modes

- `evaluation_mode=multi_turn`
  - history is rendered as real `user/assistant` turns.
- `evaluation_mode=single_turn_flattened`
  - history is flattened into one long prompt before the final target question.
- `history_mode=oracle_history`
  - dummy turns contain the gold canonical answer.
- `history_mode=self_history`
  - dummy turns contain the model's own parsed canonical answer.
- `dummy_type=same_domain`
  - dummy questions come from the same subject/domain as the target.
- `dummy_type=cross_domain`
  - dummy questions come from a different subject/domain (or a different dataset pool).

---

## 2. Repository structure

```text
configs/                  YAML experiment configs
data/
  fixtures/               Local JSONL fixtures for smoke tests
  cache/                  Optional Hugging Face dataset cache (created at runtime)
logs/                     Per-run log files
results/
  manifests/              Fixed target→dummy sampling manifests
  runs/                   Run-specific JSON + partial JSONL outputs
  summary/                Cumulative CSV scoreboard
scripts/                  Shell helpers for env setup and runs
src/crb/
  cli/                    CLI entrypoints
  datasets/               Dataset adapters and normalization
  engines/                Inference backends (vLLM, mock)
  evaluation/             Parsers, scorers, orchestration
  io/                     Result writers
  prompts/                Prompt rendering
  sampling/               Dummy pack / manifest generation
  utils/                  Hashing, git metadata, runtime helpers
tests/                    Parser/sampler/pipeline tests
environment.yml          Conda environment definition
requirements.txt         Pip dependency pins
pyproject.toml           Editable install + CLI entrypoints
README.md                This file
```

---

## 3. Supported datasets

### Implemented now
- **MMLU-style multiple-choice** via `adapter: mmlu`
  - default example config uses `cais/mmlu` as an MMLU-family knowledge benchmark.
- **GSM8K** via `adapter: gsm8k`
- **GPQA** via `adapter: gpqa`
- **Local JSONL fixtures** via `adapter: jsonl` for smoke testing and CI-like checks

### Internal normalized format
Each dataset adapter converts raw records into a common schema:

```json
{
  "dataset_name": "...",
  "split": "...",
  "item_id": "...",
  "domain": "...",
  "subject": "...",
  "question": "...",
  "choices": ["..."],
  "answer": "...",
  "answer_type": "mcq | numeric | freeform"
}
```

This makes it easy to add new adapters later.

---

## 4. Environment setup

## Recommended environment
- Conda env name: `crb`
- Python: **3.12**
- Primary backend: **vLLM 0.11.x**
- Transformers: **4.51+**

This project prefers a compatibility-first stack over bleeding-edge pins.

### Create the conda env

```bash
cd /data_x/aa007878/projects/crb
bash scripts/create_conda_env.sh
conda activate crb
pip install -e .
```

> Note: this repo uses `CONDA_NO_PLUGINS=true` in the helper script because this machine's base conda installation can fail during CUDA virtual-package detection under sandboxed execution.

### Manual environment creation

```bash
CONDA_NO_PLUGINS=true conda env create -f environment.yml
conda activate crb
pip install -e .
```

### Dependency files
- `environment.yml`
- `requirements.txt`
- `pyproject.toml`

---

## 5. vLLM / CUDA notes

This repository is designed around the **vLLM Python API** rather than an external OpenAI-compatible server.

Why:
- easier experiment automation from Python
- no separate server lifecycle to coordinate
- simpler config-driven tensor parallel control
- easier per-run logging and exception handling

### GPU defaults
The provided shell scripts default to:
- single GPU: `CUDA_VISIBLE_DEVICES=6`
- multi GPU: `CUDA_VISIBLE_DEVICES=6,7`

### Single GPU
```bash
bash scripts/run_single_gpu.sh configs/qwen25_1p5b_mmlu_multiturn_oracle_k2.yaml
```

### Multi GPU
```bash
bash scripts/run_multi_gpu.sh configs/qwen25_1p5b_gsm8k_flattened_self_k2.yaml
```

### Batch execution
```bash
bash scripts/run_batch.sh configs/
```

### Tensor parallel behavior
Set in YAML with:
```yaml
model:
  tensor_parallel_size: auto
```

`auto` resolves from `CUDA_VISIBLE_DEVICES`, so the same config can run unchanged on:
- `CUDA_VISIBLE_DEVICES=6`
- `CUDA_VISIBLE_DEVICES=6,7`

---

## 6. CLI entrypoints

### Run an evaluation
```bash
python -m crb.cli.run_eval --config configs/qwen25_1p5b_mmlu_multiturn_oracle_k2.yaml
```

### Generate or reuse a manifest only
```bash
python -m crb.cli.generate_pack --config configs/qwen25_1p5b_mmlu_multiturn_oracle_k2.yaml
```

### Run multiple configs
```bash
python -m crb.cli.run_batch configs/qwen25_1p5b_mmlu_multiturn_oracle_k2.yaml configs/qwen25_1p5b_gsm8k_flattened_self_k2.yaml
```

After editable install, you can also use:
- `crb-eval`
- `crb-pack`
- `crb-batch`

---

## 7. Config structure

Example:

```yaml
experiment:
  name: qwen25_1p5b_mmlu_multiturn_oracle_k2
  seed: 42
  num_samples: 8

model:
  engine: vllm
  model_name: Qwen/Qwen2.5-1.5B-Instruct
  tensor_parallel_size: auto

prompt:
  system_prompt: "..."
  final_answer_instruction: "..."

evaluation:
  evaluation_mode: multi_turn
  history_mode: oracle_history
  dummy_type: same_domain
  k: 2
  manifest_k_values: [0, 2, 4, 8]
  target:
    dataset_name: mmlu
    adapter: mmlu
    path: cais/mmlu
    subset: all
    split: test
  dummy_sources:
    - dataset_name: mmlu
      adapter: mmlu
      path: cais/mmlu
      subset: all
      split: validation
```

### Important axes controlled by config
- model name
- decoding params
- prompt template
- target dataset / split
- dummy pool datasets / splits
- `evaluation_mode`
- `history_mode`
- `dummy_type`
- `k`
- `seed`
- `num_samples`
- resume / skip / timeout behavior

---

## 8. Reproducible dummy sampling

CRB precomputes a **model-independent evaluation manifest**.

For each target item:
1. build a candidate dummy pool
2. filter by same-domain or cross-domain rules
3. exclude duplicates / target leakage
4. sample deterministically from seed + target id
5. save the manifest to `results/manifests/*.json`

This guarantees that different models reuse the same target→dummy assignments.

### Manifest behavior
- manifests are reused automatically if they already exist
- `k` is selected from the front of a pre-sampled ordered dummy list
- the manifest is saved before model evaluation begins

---

## 9. Prompting and answer extraction

### Output contract
All prompts instruct the model to end with:

- MCQ: `Answer: B`
- Numeric: `Answer: 42`

### History storage default
History stores the **canonicalized answer**, not the full raw generation.

### Parsing
Implemented as:
- strict parser first
- fallback parser second
- explicit invalid / ambiguous failure logging

### Scoring
- MCQ: exact canonical letter match
- Numeric: exact rationally-normalized match (`0.5 == 1/2`)
- No reprompting

---

## 10. Output files

## Run-level JSON
Each completed run writes one JSON file under:

```text
results/runs/<experiment>__<config_hash>/run-<timestamp>-<short_hash>.json
```

Contents include:
- run metadata
- git commit
- config snapshot
- metrics
- per-item results
- raw output
- parsed answer
- gold answer
- dummy ids / dummy turns
- error type

## Partial JSONL for resume
During execution:

```text
results/runs/<experiment>__<config_hash>/partial_results.jsonl
```

## Cumulative CSV scoreboard
A single CSV is appended at:

```text
results/summary/scoreboard.csv
```

Columns:
- `timestamp`
- `run_id`
- `git_commit`
- `model_name`
- `dataset`
- `split`
- `evaluation_mode`
- `history_mode`
- `dummy_type`
- `k`
- `seed`
- `num_items`
- `accuracy`
- `format_failure_rate`
- `result_json_path`

---

## 11. Resume / skip / failure handling

Implemented protections:
- deterministic config hashing
- reusable manifests
- partial per-item JSONL writes
- resume from partial outputs
- skip completed runs (`skip_completed: true`)
- per-item exception capture
- timeout support via `runtime.timeout_seconds`
- per-run log file under `logs/`

If a model call fails, CRB records a runtime failure entry rather than silently dropping the item.

---

## 12. Included configs

### Smoke / local fixture configs
- `configs/mock_mmlu_multiturn_oracle.yaml`
- `configs/mock_gsm8k_flattened_self.yaml`

These use the mock engine and local JSONL fixtures to validate the full pipeline without GPU inference.

### Real vLLM configs
- `configs/qwen25_1p5b_mmlu_multiturn_oracle_k2.yaml`
- `configs/qwen25_1p5b_gsm8k_flattened_self_k2.yaml`

These are intended for actual GPU-backed runs.

---

## 13. Quick verification commands

### Local smoke check
```bash
PYTHONPATH=src python -m crb.cli.run_eval --config configs/mock_mmlu_multiturn_oracle.yaml
PYTHONPATH=src python -m crb.cli.run_eval --config configs/mock_gsm8k_flattened_self.yaml
```

### Manifest-only test
```bash
PYTHONPATH=src python -m crb.cli.generate_pack --config configs/mock_mmlu_multiturn_oracle.yaml
```

### Bytecode sanity check
```bash
python -m compileall src tests
```

---

## 14. Extending the system

### Add a new dataset
1. create a loader in `src/crb/datasets/`
2. normalize records into `NormalizedItem`
3. register the adapter in the dataset registry
4. add a YAML config

### Add a new model
1. duplicate a config
2. change `model.model_name`
3. optionally adjust decoding / tensor parallel settings

### Add a new evaluation variant
Likely extension points:
- prompt templates in `src/crb/prompts/`
- evaluation orchestration in `src/crb/evaluation/runner.py`
- new parser / scorer in `src/crb/evaluation/`

---

## 15. Current implementation status

Implemented:
- project scaffold and editable Python package
- config-driven experiment runner
- normalized dataset schema
- MMLU / GSM8K / GPQA loaders
- dummy-pack manifest generation
- multi-turn + flattened prompting
- self-history + oracle-history modes
- per-run JSON writing
- cumulative CSV scoreboard
- single-/multi-GPU shell entrypoints
- smoke-test fixture configs

Pending or expected next validation steps:
- install/verify vLLM inside the dedicated conda env
- run real GPU-backed experiments on at least two datasets
- confirm final single-GPU and multi-GPU end-to-end results on this machine

---

## 16. Git workflow expectation

Recommended checkpoint commits for this repo:
- scaffold / env / README
- dataset + manifest layer
- evaluation pipeline + outputs
- GPU validation + README update

