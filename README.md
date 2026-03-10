# CRB: Conversation-Accumulated / Multi-Turn Interference Benchmark

CRB is a reproducible experiment pipeline for measuring how a model's answer to a **final target problem** changes after accumulating **dummy question-answer turns** in prior conversation history.

The benchmark supports:
- **multi-turn accumulated evaluation**
- **single-turn flattened control**
- **self-history vs oracle-history**
- **same-domain vs cross-domain dummy histories**
- **k-shot dummy history sweeps**
- **run-level JSON outputs**
- **cumulative CSV scoreboard logging**
- **reusable, model-independent evaluation pack manifests**
- **Qwen3 thinking on/off comparisons**

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
   - model reasoning modes such as **Qwen3 thinking on/off**

### Core evaluation modes

- `evaluation_mode=multi_turn`
  - history is rendered as real `user/assistant` turns.
- `evaluation_mode=single_turn_flattened`
  - history is flattened into one long prompt before the final target question.
- `history_mode=oracle_history`
  - dummy turns contain the gold canonical answer.
- `history_mode=self_history`
  - dummy turns contain the model's own parsed canonical answer.

### Dummy domain policy

CRB normalizes every sample into a common `domain` + `subject` schema.

- `dummy_type=same_domain`
  - dummy questions must share either the same normalized `subject` or the same normalized broad `domain` as the target.
- `dummy_type=cross_domain`
  - dummy questions must **not** share the same normalized `subject` or broad `domain` as the target.
  - cross-dataset dummies are allowed, but they are **not automatically cross-domain** unless the normalized domain actually differs.

### Important edge case: AIME / math-heavy settings

AIME is almost entirely `domain=math`, so meaningful `cross_domain` evaluation usually requires **cross-dataset dummy pools** such as GPQA or MMLU non-math subjects. This is supported by the default AIME configs.

---

## 2. Repository structure

```text
configs/
  templates/              Base templates for paper-scale sweeps
  sweeps/                 Sweep specs that expand into concrete configs
  *.yaml                  Hand-authored run configs
data/
  fixtures/               Local JSONL fixtures for smoke tests
  cache/                  Optional Hugging Face dataset cache (created at runtime)
logs/                     Per-run log files
results/
  manifests/              Fixed target→dummy sampling manifests
  runs/                   Run-specific JSON + partial JSONL outputs
  summary/                Cumulative CSV scoreboard
scripts/                  Shell helpers for env setup, batching, and sweep materialization
src/crb/
  cli/                    CLI entrypoints
  datasets/               Dataset adapters and normalization
  engines/                Inference backends (vLLM, mock)
  evaluation/             Parsers, scorers, orchestration
  io/                     Result writers
  prompts/                Prompt rendering
  sampling/               Dummy pack / manifest generation
  utils/                  Hashing, git metadata, runtime helpers
tests/                    Parser/sampler/config metadata tests
environment.yml          Conda environment definition
requirements.txt         Pip dependency pins
pyproject.toml           Editable install + CLI entrypoints
README.md                This file
```

---

## 3. Supported datasets

### Currently supported adapters
- **MMLU-family** via `adapter: mmlu`
  - current default example uses `cais/mmlu`
- **GSM8K** via `adapter: gsm8k`
- **GPQA** via `adapter: gpqa`
  - current configs use `Idavidrein/gpqa`
- **AIME** via `adapter: aime`
  - current configs use `HuggingFaceH4/aime_2024`
- **Local JSONL fixtures** via `adapter: jsonl`

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

### Dataset-specific notes

#### MMLU-family
- normalized as `mcq`
- `subject` comes from the benchmark subject
- `domain` is broad-normalized by keyword heuristics (for example, math / physics / chemistry / law / history)

#### GSM8K
- normalized as `numeric`
- `domain=math`
- `subject=arithmetic`

#### GPQA
- normalized as `mcq`
- uses `High-level domain` and `Subdomain` where available
- answer choices are **deterministically shuffled per item** so the correct answer is not always `A`
- this preserves reproducibility while making the evaluation more realistic

#### AIME
- normalized as `numeric`
- `domain=math`
- `subject=aime`
- answer extraction uses the numeric evaluator, which supports stripping extra punctuation and normalizing integers / decimals / fractions before exact comparison

---

## 4. Environment setup

## Recommended environment
- project-local conda env: `/data_x/aa007878/projects/crb/.conda/envs/crb`
- Python: **3.10**
- primary backend: **vLLM 0.11.2**
- Torch: **2.9.0+cu128**
- Transformers: **4.57.6**

This project prefers a compatibility-first stack over bleeding-edge pins.

All setup and run scripts export `PYTHONNOUSERSITE=1` to prevent accidental leakage from user-level site-packages on this machine.

### Create the conda env

```bash
cd /data_x/aa007878/projects/crb
bash scripts/create_conda_env.sh
conda activate /data_x/aa007878/projects/crb/.conda/envs/crb
```

### Manual environment creation

```bash
CONDA_NO_PLUGINS=true conda create -y -p /data_x/aa007878/projects/crb/.conda/envs/crb python=3.10 pip
conda activate /data_x/aa007878/projects/crb/.conda/envs/crb
PYTHONNOUSERSITE=1 pip install -r requirements.txt
PYTHONNOUSERSITE=1 pip install -e .
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

## 6. Qwen3 thinking on / off support

CRB now supports **same-family, same-size Qwen3 comparisons** using config-level thinking control.

### Implementation strategy

For Qwen3 configs, CRB stores:
- `model.model_family: qwen3`
- `model.thinking_mode: on | off`
- `model.chat_template_kwargs.enable_thinking: true | false`

At prompt rendering time, the vLLM engine forwards `chat_template_kwargs` to `tokenizer.apply_chat_template(...)`.

This means:
- **thinking off** is a hard config-level switch via `enable_thinking: false`
- **thinking on** is a hard config-level switch via `enable_thinking: true`
- `thinking_mode` is recorded in both run JSON and the cumulative CSV scoreboard

### Included Qwen3 comparison configs

- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`

### Qwen3 decoding presets

The configs use separate decoding defaults for paper comparisons:
- **thinking off**: `temperature=0.7`, `top_p=0.8`, `top_k=20`
- **thinking on**: `temperature=0.6`, `top_p=0.95`, `top_k=20`

These are encoded directly in the config files and sweep presets.

---

## 7. CLI entrypoints

### Run an evaluation
```bash
python -m crb.cli.run_eval --config configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml
```

### Generate or reuse a manifest only
```bash
python -m crb.cli.generate_pack --config configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml
```

### Run multiple configs
```bash
python -m crb.cli.run_batch \
  configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml \
  configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml
```

### Materialize the paper sweep into concrete configs
```bash
python -m crb.cli.materialize_sweep --spec configs/sweeps/qwen3_core_paper.yaml
```

After editable install, you can also use:
- `crb-eval`
- `crb-pack`
- `crb-batch`
- `crb-materialize`

---

## 8. Config structure

Example:

```yaml
experiment:
  name: qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on
  seed: 42
  num_samples: 8

model:
  engine: vllm
  model_name: Qwen/Qwen3-1.7B
  model_family: qwen3
  thinking_mode: on
  tensor_parallel_size: auto
  chat_template_kwargs:
    enable_thinking: true

decoding:
  temperature: 0.6
  top_p: 0.95
  top_k: 20
  max_tokens: 2048

evaluation:
  evaluation_mode: multi_turn
  history_mode: oracle_history
  dummy_type: same_domain
  k: 2
```

### Important axes controlled by config
- model name
- model family
- thinking mode
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

## 9. Paper-scale sweep setup

CRB now includes **paper sweep templates** and a **materialization spec** so that full experiments can be expanded consistently before batch execution.

### Base templates

- `configs/templates/qwen3_1p7b_mmlu_base.yaml`
- `configs/templates/qwen3_1p7b_gsm8k_base.yaml`
- `configs/templates/qwen3_1p7b_gpqa_base.yaml`
- `configs/templates/qwen3_1p7b_aime_base.yaml`

### Core sweep spec

- `configs/sweeps/qwen3_core_paper.yaml`

This sweep covers:
- datasets: `mmlu`, `gsm8k`, `gpqa`, `aime`
- evaluation modes: `multi_turn`, `single_turn_flattened`
- history modes: `oracle_history`, `self_history`
- dummy types: `same_domain`, `cross_domain`
- `k`: `0, 2, 4, 8`
- thinking modes: `on`, `off`

### Materialize + run flow

```bash
bash scripts/materialize_qwen3_core_sweep.sh
bash scripts/run_qwen3_core_sweep.sh
```

The generated configs are written to:

```text
configs/generated/qwen3_core_paper/
```

This keeps the paper sweep reproducible while avoiding a large hand-maintained matrix of YAML files.

---

## 10. Reproducible dummy sampling

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
- manifests stay **model-independent**

---

## 11. Prompting and evaluators

### Output contract
All prompts instruct the model to end with:

- MCQ: `Answer: B`
- Numeric: `Answer: 42`

### History storage default
History stores the **canonicalized answer**, not the full raw generation.

### MCQ evaluator
- strict parser first
- fallback parser second
- extracts canonical choice letters `A`–`J`
- ambiguous or conflicting outputs become invalid

### Numeric evaluator
- strips extra punctuation / spaces / commas
- normalizes integers, decimals, and fractions
- exact match is performed on the normalized canonical form
- useful for GSM8K and AIME-style integer answers

---

## 12. Output files

## Run-level JSON
Each completed run writes one JSON file under:

```text
results/runs/<experiment>__<config_hash>/run-<timestamp>-<short_hash>.json
```

### Top-level JSON fields
CRB now records:
- `run_id`
- `timestamp`
- `git_commit`
- `model_name`
- `model_family`
- `thinking_mode`
- `engine`
- `dataset`
- `split`
- `evaluation_mode`
- `history_mode`
- `dummy_type`
- `k`
- `seed`
- `num_items`
- `metrics`
- `config`
- `per_item_results`

### Per-item fields
Each item result includes:
- `item_id`
- target `domain` / `subject`
- `dummy_ids`
- `dummy_domains`
- `dummy_subjects`
- `dummy_dataset_names`
- `history_construction_mode`
- `raw_output`
- `parsed_answer`
- `gold_answer`
- `normalized_gold_answer`
- `correct`
- `parse_status`
- `parser_name`
- `error_type`

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

### Scoreboard columns
- `timestamp`
- `run_id`
- `git_commit`
- `model_name`
- `model_family`
- `thinking_mode`
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

## 13. Resume / skip / failure handling

Implemented protections:
- deterministic config hashing
- reusable manifests
- partial per-item JSONL writes
- resume from partial outputs
- skip completed runs (`skip_completed: true`)
- per-item exception capture
- timeout support via `runtime.timeout_seconds`
- per-run log file under `logs/`
- scoreboard header migration when new metadata fields are added

If a model call fails, CRB records a runtime failure entry rather than silently dropping the item.

---

## 14. Included configs

### Smoke / local fixture configs
- `configs/mock_mmlu_multiturn_oracle.yaml`
- `configs/mock_gsm8k_flattened_self.yaml`

### Earlier validated Qwen2.5 configs
- `configs/qwen25_1p5b_mmlu_multiturn_oracle_k2.yaml`
- `configs/qwen25_1p5b_gsm8k_flattened_self_k2.yaml`

### New Qwen3 configs
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_off.yaml`
- `configs/qwen3_1p7b_gsm8k_flattened_self_cross_k2_thinking_on.yaml`
- `configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml`

---

## 15. Verification and current status

Already validated earlier in this repository:
- project-local conda env at `/data_x/aa007878/projects/crb/.conda/envs/crb`
- single-GPU path with `CUDA_VISIBLE_DEVICES=6`
- multi-GPU path with `CUDA_VISIBLE_DEVICES=6,7`
- real vLLM run on an MMLU-family benchmark
- real vLLM run on GSM8K
- run JSON creation under `results/runs/`
- cumulative scoreboard append under `results/summary/scoreboard.csv`

Current repository expansion in this phase:
- GPQA adapter hardened for deterministic choice ordering
- AIME adapter added
- Qwen3 thinking on/off metadata and chat-template controls added
- paper sweep materialization support added
- JSON / scoreboard metadata expanded with `model_family` and `thinking_mode`

### Important current operational note
At the time of this update, GPU contention took priority over additional runtime validation. The new GPQA / AIME / Qwen3 configs and sweep tooling are committed and ready, but **additional GPU-backed execution should be resumed when GPUs 6 and 7 are free**.

---

## 16. Quick commands to use later when GPUs are free

### GPQA / Qwen3 thinking off
```bash
bash scripts/run_single_gpu.sh configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml
```

### GPQA / Qwen3 thinking on
```bash
bash scripts/run_single_gpu.sh configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml
```

### AIME / Qwen3 thinking off
```bash
bash scripts/run_single_gpu.sh configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml
```

### Materialize the full paper sweep
```bash
bash scripts/materialize_qwen3_core_sweep.sh
```

### Run the full materialized sweep
```bash
bash scripts/run_qwen3_core_sweep.sh
```

---

## 17. Known limitations / TODO

- the new GPQA / AIME / Qwen3 configs are added, but this phase intentionally defers additional GPU runs until contention clears
- the paper sweep spec is ready, but the generated configs are not checked into git by default
- AIME is treated as `domain=math`, so meaningful `cross_domain` experiments require cross-dataset dummy pools
- numeric evaluation is exact-match after normalization; more advanced symbolic equivalence is not implemented yet
- the current Qwen3 support focuses on config-level `enable_thinking`; prompt-level soft control like `/think` or `/no_think` is not the main paper path

---

## 18. Git workflow expectation

Recommended checkpoint commits for this repo:
- scaffold / env / README
- dataset + manifest layer
- evaluation pipeline + outputs
- benchmark expansion + reasoning mode support
- final GPU validation pass when resources are free
