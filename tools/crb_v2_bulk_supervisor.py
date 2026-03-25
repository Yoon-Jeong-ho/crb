from __future__ import annotations

import argparse
import csv
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from crb_v2.artifacts import experiment_root
from crb_v2.catalog import BENCHMARK_SPECS
from crb_v2.config import load_pipeline_config

ROOT = Path(__file__).resolve().parents[1]
STATUS_DIR = ROOT / "results_v2" / "manifests" / "status"
QUEUE_DIR = ROOT / "results_v2" / "manifests" / "queues"
SUMMARY_DIR = ROOT / "results_v2" / "summary"
ANALYSIS_DIR = ROOT / "analysis_v2" / "tables"
GENERATED_BUNDLE_DIR = ROOT / "configs_v2" / "generated" / "bundles"
WORKER_LOG_DIR = ROOT / "logs" / "crb_v2" / "workers"
JOB_LOG_DIR = ROOT / "logs" / "crb_v2" / "jobs"
STATE_PATH = STATUS_DIR / "job_state.json"
STATE_LOCK_PATH = STATUS_DIR / "job_state.lock"
WORKER_STATE_PATH = STATUS_DIR / "workers.json"
PAIR67_LOCK_PATH = STATUS_DIR / "tp2_gpu67.lock"
PYTHON = ROOT / ".conda" / "envs" / "crb" / "bin" / "python"
REFRESH_SCRIPT = ROOT / "scripts_v2" / "refresh_v2_inventory.sh"

BENCHMARK_ORDER = [
    "gsm8k",
    "math500",
    "gpqa",
    "arc_challenge",
    "mmlu_pro",
    "mmlu_redux_2",
    "hellaswag",
    "piqa",
    "boolq",
    "truthfulqa_mc",
]
K_VALUES = [0, 1, 2, 4, 8, 16, 32]
RELATIONS = ["same_benchmark", "same_domain_other_benchmark", "cross_domain"]
PROVENANCES = ["model_correct", "model_incorrect"]
RETRYABLE_FAILURES = {"engine_death", "startup_failure", "cancelled", "transient_file_issue", "unknown"}
TRANSIENT_FILE_MARKERS = ["temporarily unavailable", "resource busy", "file exists", "stale file handle"]
HEAVY_BUCKETS = {"retry_tp2"}
PROBATION_BUCKETS = {"bulk_unverified"}
BLOCKED_BUCKETS = {"retry_blocked"}
STABLE_BUCKETS = {"bulk_ready"}
MAX_RETRIES = 3
SUMMARY_REFRESH_SECONDS = 60
IDLE_SLEEP_SECONDS = 5
ACTIVE_GPUS = {"4", "5", "6"}


@dataclass
class JobRecord:
    job_id: str
    model: str
    benchmark: str
    split: str
    condition_bundle: str
    queue_name: str
    priority: int
    gpu_id: str
    status: str
    retry_count: int
    failure_type: str
    config_path: str
    log_path: str
    output_dir: str
    pool_status: str
    started_at: str
    finished_at: str
    next_retry_at: str
    notes: str
    preferred_gpu: str
    allowed_gpus: str
    recipe_class: str


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_epoch() -> float:
    return datetime.now(timezone.utc).timestamp()


def parse_time(value: str) -> float | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        return None


def ensure_dirs() -> None:
    for path in [STATUS_DIR, QUEUE_DIR, SUMMARY_DIR, ANALYSIS_DIR, GENERATED_BUNDLE_DIR, WORKER_LOG_DIR, JOB_LOG_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    for gpu in ["4", "5", "6", "7"]:
        (JOB_LOG_DIR / f"gpu{gpu}").mkdir(parents=True, exist_ok=True)


class LockedState:
    def __enter__(self) -> dict[str, Any]:
        ensure_dirs()
        self.handle = STATE_LOCK_PATH.open("a+", encoding="utf-8")
        fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX)
        if STATE_PATH.exists():
            self.state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        else:
            self.state = {"created_at": utc_now(), "updated_at": utc_now(), "jobs": []}
        return self.state

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is None:
            self.state["updated_at"] = utc_now()
            tmp_path = STATE_PATH.with_suffix(".json.tmp")
            tmp_path.write_text(json.dumps(self.state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            os.replace(tmp_path, STATE_PATH)
            write_state_views(self.state)
        fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        self.handle.close()


def model_inventory_rows() -> list[dict[str, str]]:
    path = ANALYSIS_DIR / "models_inventory.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing models inventory: {path}")
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


MODEL_ROWS_BY_KEY: dict[str, dict[str, str]] = {}


def refresh_model_rows() -> None:
    MODEL_ROWS_BY_KEY.clear()
    for row in model_inventory_rows():
        MODEL_ROWS_BY_KEY[row["model_key"]] = row


def bundle_priority(model: str, benchmark: str, execution_bucket: str) -> int:
    benchmark_idx = BENCHMARK_ORDER.index(benchmark)
    stable_models = [
        "qwen25_7b_instruct",
        "llama31_8b_instruct",
        "mistral7b_instruct_v03",
        "phi4_mini_instruct",
        "deepseek_r1_distill_qwen_7b",
        "mistral_small_24b_instruct_2501",
        "qwq_32b",
        "deepseek_r1_distill_llama_8b",
        "olmo2_1124_7b_instruct",
    ]
    model_idx = stable_models.index(model) if model in stable_models else 99
    base = benchmark_idx * 100 + model_idx
    if execution_bucket in PROBATION_BUCKETS:
        base += 10000
    if execution_bucket in HEAVY_BUCKETS:
        base += 5000
    if execution_bucket in BLOCKED_BUCKETS:
        base += 20000
    return base


def queue_name_for_bucket(bucket: str) -> str:
    if bucket in HEAVY_BUCKETS and "7" not in ACTIVE_GPUS:
        return "blocked"
    if bucket in PROBATION_BUCKETS:
        return "probation_queue"
    if bucket in BLOCKED_BUCKETS:
        return "blocked"
    return "main_bulk_queue"


def recipe_class_for_bucket(bucket: str) -> str:
    if bucket in PROBATION_BUCKETS:
        return "runtime_unverified"
    if bucket in HEAVY_BUCKETS:
        return "needs_tp2"
    if bucket in BLOCKED_BUCKETS:
        return "blocked"
    return "stable_single_gpu"


def allowed_gpus_for_recipe(recipe_class: str, preferred_gpu: str) -> str:
    if recipe_class == "stable_single_gpu":
        return "4|5"
    if recipe_class == "needs_tp2":
        return ""
    if recipe_class == "runtime_unverified":
        return "4|5|6"
    return ""


def preferred_gpu_for(model: str, recipe_class: str) -> str:
    if recipe_class == "stable_single_gpu":
        gpu4_models = {"qwen25_7b_instruct", "mistral7b_instruct_v03", "deepseek_r1_distill_qwen_7b"}
        return "4" if model in gpu4_models else "5"
    if recipe_class in {"needs_tp2", "runtime_unverified"}:
        return "6"
    return ""


def build_bundle_config(model: str, benchmark: str, tp_size: int) -> dict[str, Any]:
    split = BENCHMARK_SPECS[benchmark].split
    max_new_tokens = 192 if MODEL_ROWS_BY_KEY[model]["model_type"] == "reasoning" else 128
    return {
        "experiment_name": f"crb_v2_bundle__{model}__{benchmark}",
        "models": [
            {
                "key": model,
                "tensor_parallel_size": tp_size,
                "max_new_tokens": max_new_tokens,
            }
        ],
        "benchmarks": [
            {
                "key": benchmark,
                "split": split,
            }
        ],
        "pool_policy": {
            "require_full_benchmark": False,
            "min_correct": 50,
            "min_incorrect": 50,
        },
        "sweep": {
            "k_values": K_VALUES,
            "relations": RELATIONS,
            "provenances": PROVENANCES,
        },
        "output": {"root_dir": "results_v2", "overwrite": False, "resume": True},
        "runtime": {"seed": 42, "timeout_seconds": 300},
    }


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def predicted_output_dir(config_path: Path) -> Path:
    config = load_pipeline_config(config_path)
    target = experiment_root(config)
    return target if target.is_absolute() else (ROOT / target)


def job_id_for(model: str, benchmark: str) -> str:
    return f"bundle::{model}::{benchmark}::tier1"


def initial_job_rows() -> list[JobRecord]:
    refresh_model_rows()
    rows: list[JobRecord] = []
    for model in [row["model_key"] for row in model_inventory_rows()]:
        meta = MODEL_ROWS_BY_KEY[model]
        bucket = meta["execution_bucket"]
        recipe_class = recipe_class_for_bucket(bucket)
        preferred_gpu = preferred_gpu_for(model, recipe_class)
        allowed_gpus = allowed_gpus_for_recipe(recipe_class, preferred_gpu)
        tp_size = int(meta["preferred_tp"])
        for benchmark in BENCHMARK_ORDER:
            config_path = GENERATED_BUNDLE_DIR / model / f"{benchmark}.yaml"
            config_payload = build_bundle_config(model, benchmark, tp_size)
            write_yaml(config_path, config_payload)
            output_dir = predicted_output_dir(config_path)
            log_path = JOB_LOG_DIR / f"gpu{preferred_gpu or 'x'}" / f"{model}__{benchmark}.log"
            queue_name = queue_name_for_bucket(bucket)
            status = "queued"
            notes = meta["evidence"]
            if queue_name == "blocked":
                status = "blocked"
            if (output_dir / "pipeline_result.json").exists() and (output_dir / "aggregate" / "summary_rows.csv").exists():
                status = classify_completion_status(output_dir)
                queue_name = "done"
            rows.append(
                JobRecord(
                    job_id=job_id_for(model, benchmark),
                    model=model,
                    benchmark=benchmark,
                    split=BENCHMARK_SPECS[benchmark].split,
                    condition_bundle="single_turn_plus_tier1_contamination",
                    queue_name=queue_name,
                    priority=bundle_priority(model, benchmark, bucket),
                    gpu_id="",
                    status=status,
                    retry_count=0,
                    failure_type="",
                    config_path=str(config_path.relative_to(ROOT)),
                    log_path=str(log_path.relative_to(ROOT)),
                    output_dir=str(output_dir.relative_to(ROOT)),
                    pool_status="",
                    started_at="",
                    finished_at="",
                    next_retry_at="",
                    notes=notes,
                    preferred_gpu=preferred_gpu,
                    allowed_gpus=allowed_gpus,
                    recipe_class=recipe_class,
                )
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_state_views(state: dict[str, Any]) -> None:
    jobs = state.get("jobs", [])
    fieldnames = [
        "job_id", "model", "benchmark", "split", "condition_bundle", "queue_name", "priority", "gpu_id", "status", "retry_count",
        "failure_type", "config_path", "log_path", "output_dir", "pool_status", "started_at", "finished_at", "next_retry_at", "notes",
        "preferred_gpu", "allowed_gpus", "recipe_class",
    ]
    write_csv(STATUS_DIR / "job_status.csv", jobs, fieldnames)
    write_json(STATUS_DIR / "job_status.json", jobs)

    queue_payload = {
        "main_bulk_queue": [job for job in jobs if job["queue_name"] == "main_bulk_queue" and job["status"] in {"queued", "claimed", "running", "retry_wait"}],
        "probation_queue": [job for job in jobs if job["queue_name"] == "probation_queue" and job["status"] in {"queued", "claimed", "running", "retry_wait"}],
        "retry_queue": [job for job in jobs if job["queue_name"] == "retry_queue" and job["status"] in {"queued", "claimed", "running", "retry_wait"}],
        "blocked": [job for job in jobs if job["status"] in {"blocked", "failed_permanent"}],
    }
    for queue_name, queue_jobs in queue_payload.items():
        write_json(QUEUE_DIR / f"{queue_name}.json", queue_jobs)
        write_csv(
            QUEUE_DIR / f"{queue_name}.csv",
            queue_jobs,
            ["job_id", "model", "benchmark", "queue_name", "priority", "status", "retry_count", "failure_type", "config_path", "output_dir", "notes", "preferred_gpu", "allowed_gpus", "recipe_class"],
        )

    coverage = coverage_summary(jobs)
    write_json(SUMMARY_DIR / "bulk_coverage_summary.json", coverage)
    write_csv(SUMMARY_DIR / "bulk_coverage_summary.csv", [coverage], list(coverage.keys()))
    write_json(STATUS_DIR / "queue_snapshot.json", {key: len(value) for key, value in queue_payload.items()})


def coverage_summary(jobs: list[dict[str, Any]]) -> dict[str, Any]:
    total = len([job for job in jobs if job["status"] != "blocked"])
    single_turn_done = len([job for job in jobs if job["status"] in {"completed", "partial_complete", "skipped"} and job.get("pool_status")])
    contamination_started = len([job for job in jobs if job["status"] in {"completed", "partial_complete"}])
    completed = len([job for job in jobs if job["status"] == "completed"])
    partial = len([job for job in jobs if job["status"] == "partial_complete"])
    retries = len([job for job in jobs if job["status"] == "retry_wait"])
    running = len([job for job in jobs if job["status"] in {"claimed", "running"}])
    skipped = len([job for job in jobs if job["status"] == "skipped"])
    blocked = len([job for job in jobs if job["status"] in {"blocked", "failed_permanent"}])
    benchmark_coverage = {benchmark: 0 for benchmark in BENCHMARK_ORDER}
    for job in jobs:
        if job["status"] in {"completed", "partial_complete", "skipped"}:
            benchmark_coverage[job["benchmark"]] += 1
    coverage_ratio = round((contamination_started / total), 4) if total else 0.0
    return {
        "generated_at": utc_now(),
        "total_jobs": total,
        "single_turn_done": single_turn_done,
        "contamination_started": contamination_started,
        "completed": completed,
        "partial_complete": partial,
        "running_or_claimed": running,
        "retry_wait": retries,
        "skipped": skipped,
        "blocked_or_failed_permanent": blocked,
        "coverage_ratio": coverage_ratio,
        **{f"coverage_{benchmark}": count for benchmark, count in benchmark_coverage.items()},
    }


def classify_failure(log_text: str, exit_code: int, recipe_class: str) -> tuple[str, bool, str]:
    lower = log_text.lower()
    if "out of memory" in lower or "cuda oom" in lower or "oom" in lower:
        return "oom", False, "OOM detected; same recipe will not be retried automatically"
    if "engine core initialization failed" in lower or "died unexpectedly" in lower or "enginecore" in lower:
        return "engine_death", True, "vLLM engine death detected"
    if "cancelled" in lower:
        return "cancelled", True, "Cancelled runtime detected"
    if any(marker in lower for marker in TRANSIENT_FILE_MARKERS):
        return "transient_file_issue", True, "Transient file/runtime issue detected"
    if "traceback" in lower and "src/crb_v2" in lower:
        return "code_error", False, "Traceback points into src/crb_v2"
    if exit_code != 0:
        return "startup_failure", True, "Process exited non-zero before clean completion"
    return "unknown", True, "Unknown failure signature"


def summarize_pool_status(output_dir: Path, model: str, benchmark: str) -> str:
    baseline_summary_path = output_dir / "baseline" / model / benchmark / "summary.json"
    if not baseline_summary_path.exists():
        return "baseline_missing"
    payload = json.loads(baseline_summary_path.read_text(encoding="utf-8"))
    return f"correct={payload.get('correct_count', 0)};incorrect={payload.get('incorrect_count', 0)};parse_failure={payload.get('parse_failure_count', 0)};format_failure={payload.get('format_failure_count', 0)}"


def classify_completion_status(output_dir: Path) -> str:
    summary_rows = output_dir / "aggregate" / "summary_rows.csv"
    pipeline_result = output_dir / "pipeline_result.json"
    if pipeline_result.exists() and summary_rows.exists():
        with summary_rows.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if any(float(row.get("skipped_rate") or 0.0) > 0 for row in rows if row.get("stage") == "sweep"):
            return "partial_complete"
        return "completed"
    if (output_dir / "baseline").exists():
        return "partial_complete"
    return "failed_permanent"


def refresh_external_inventory() -> None:
    if REFRESH_SCRIPT.exists():
        subprocess.run(["bash", str(REFRESH_SCRIPT)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def apply_active_gpu_policy(state: dict[str, Any]) -> None:
    for job in state.get("jobs", []):
        if job["recipe_class"] == "needs_tp2":
            if job["status"] in {"queued", "claimed", "running", "retry_wait"}:
                job["status"] = "blocked"
                job["queue_name"] = "blocked"
                job["failure_type"] = "startup_failure" if not job["failure_type"] else job["failure_type"]
                job["notes"] = (job.get("notes", "") + ";blocked_gpu7_disabled_tp2_required").strip(";")
        elif job["recipe_class"] == "runtime_unverified":
            job["allowed_gpus"] = "4|5|6"
        elif job["recipe_class"] == "stable_single_gpu":
            job["allowed_gpus"] = "4|5"
        if job.get("gpu_id") == "7" and job["status"] in {"queued", "claimed", "running", "retry_wait"}:
            job["gpu_id"] = ""


def reconcile_stale_jobs(state: dict[str, Any]) -> None:
    now = utc_epoch()
    changed = False
    apply_active_gpu_policy(state)
    for job in state.get("jobs", []):
        if job["status"] in {"completed", "partial_complete", "skipped"} and job.get("queue_name") != "done":
            job["queue_name"] = "done"
            changed = True
    for job in state.get("jobs", []):
        pid_marker = [part for part in job.get("notes", "").split(";") if part.startswith("pid=")]
        alive = False
        if pid_marker:
            try:
                pid_value = int(pid_marker[-1].split("=", 1)[1])
                os.kill(pid_value, 0)
                alive = True
            except Exception:
                alive = False
        if job["status"] == "retry_wait" and alive:
            job["status"] = "running"
            changed = True
    for job in state.get("jobs", []):
        if job["status"] not in {"claimed", "running"}:
            continue
        started_ts = parse_time(job.get("started_at", ""))
        if started_ts is None or now - started_ts < 30:
            continue
        pid = job.get("notes", "")
        pid_marker = [part for part in pid.split(";") if part.startswith("pid=")]
        alive = False
        if pid_marker:
            try:
                pid_value = int(pid_marker[0].split("=", 1)[1])
                os.kill(pid_value, 0)
                alive = True
            except Exception:
                alive = False
        if alive:
            continue
        output_dir = ROOT / job["output_dir"]
        completion_status = classify_completion_status(output_dir)
        if completion_status in {"completed", "partial_complete"}:
            job["status"] = completion_status
            job["queue_name"] = "done"
            job["finished_at"] = utc_now()
            job["pool_status"] = summarize_pool_status(output_dir, job["model"], job["benchmark"])
            changed = True
            continue
        failure_type = "startup_failure"
        if job["retry_count"] < MAX_RETRIES:
            job["queue_name"] = "retry_queue"
            job["status"] = "retry_wait"
            job["retry_count"] += 1
            job["failure_type"] = failure_type
            job["next_retry_at"] = datetime.fromtimestamp(now + 10, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            job["notes"] = (job.get("notes", "") + ";reconciled_stale_process").strip(";")
        else:
            job["status"] = "failed_permanent"
            job["failure_type"] = failure_type
            job["finished_at"] = utc_now()
        changed = True
    if changed:
        state["updated_at"] = utc_now()


def init_state() -> None:
    refresh_external_inventory()
    jobs = [asdict(job) for job in initial_job_rows()]
    with LockedState() as state:
        state["created_at"] = utc_now()
        state["updated_at"] = utc_now()
        state["jobs"] = jobs
    refresh_external_inventory()


def pick_job_for_gpu(state: dict[str, Any], gpu: str) -> dict[str, Any] | None:
    now = utc_epoch()
    jobs = state.get("jobs", [])
    if gpu == "6":
        retry_jobs = [
            job for job in jobs
            if job["queue_name"] == "retry_queue"
            and job["status"] in {"queued", "retry_wait"}
            and (not job["next_retry_at"] or (parse_time(job["next_retry_at"]) or 0) <= now)
        ]
        retry_jobs.sort(key=lambda job: (job["priority"], job["retry_count"], job["job_id"]))
        if retry_jobs:
            return retry_jobs[0]

    main_jobs = [job for job in jobs if job["queue_name"] == "main_bulk_queue" and job["status"] == "queued"]
    probation_jobs = [job for job in jobs if job["queue_name"] == "probation_queue" and job["status"] == "queued"]

    if gpu in {"4", "5"}:
        candidates = [job for job in main_jobs if job["recipe_class"] == "stable_single_gpu" and gpu in job["allowed_gpus"].split("|")]
        preferred = [job for job in candidates if job["preferred_gpu"] == gpu]
        pool = preferred or candidates
        pool.sort(key=lambda job: (job["priority"], job["benchmark"], job["model"]))
        if pool:
            return pool[0]
        probation_fallback = [job for job in probation_jobs if gpu in job["allowed_gpus"].split("|")]
        probation_fallback.sort(key=lambda job: (job["priority"], job["benchmark"], job["model"]))
        return probation_fallback[0] if probation_fallback else None

    if gpu == "6":
        probation = [job for job in probation_jobs if gpu in job["allowed_gpus"].split("|")]
        probation.sort(key=lambda job: (job["priority"], job["benchmark"], job["model"]))
        return probation[0] if probation else None

    return None


def claim_job(gpu: str) -> dict[str, Any] | None:
    with LockedState() as state:
        reconcile_stale_jobs(state)
        job = pick_job_for_gpu(state, gpu)
        if job is None:
            return None
        for row in state["jobs"]:
            if row["job_id"] == job["job_id"]:
                row["status"] = "claimed"
                row["gpu_id"] = gpu
                row["started_at"] = utc_now()
                row["notes"] = row.get("notes", "")
                return dict(row)
    return None


def visible_devices(job: dict[str, Any], gpu: str) -> str:
    if job["recipe_class"] == "needs_tp2":
        return "6,7"
    return gpu


def try_acquire_pair67() -> Any:
    ensure_dirs()
    handle = PAIR67_LOCK_PATH.open("a+", encoding="utf-8")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return handle
    except BlockingIOError:
        handle.close()
        return None


def release_pair67(handle: Any) -> None:
    if handle is None:
        return
    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    handle.close()


def pair67_busy() -> bool:
    handle = try_acquire_pair67()
    if handle is None:
        return True
    release_pair67(handle)
    return False


def mark_running(job_id: str, gpu_id: str, pid: int) -> None:
    with LockedState() as state:
        for row in state["jobs"]:
            if row["job_id"] == job_id:
                row["status"] = "running"
                row["gpu_id"] = gpu_id
                extra = row.get("notes", "")
                row["notes"] = (extra + f";pid={pid}").strip(";")
                break


def finalize_job(job: dict[str, Any], exit_code: int, gpu_id: str) -> None:
    output_dir = ROOT / job["output_dir"]
    log_path = ROOT / job["log_path"]
    log_text = log_path.read_text(encoding="utf-8", errors="ignore")[-20000:] if log_path.exists() else ""
    status = classify_completion_status(output_dir)
    pool_status = summarize_pool_status(output_dir, job["model"], job["benchmark"]) if output_dir.exists() else ""
    with LockedState() as state:
        for row in state["jobs"]:
            if row["job_id"] != job["job_id"]:
                continue
            row["gpu_id"] = gpu_id
            row["finished_at"] = utc_now()
            row["pool_status"] = pool_status
            if exit_code == 0 and status in {"completed", "partial_complete"}:
                row["status"] = status
                row["failure_type"] = ""
                row["queue_name"] = "done"
                break
            failure_type, retryable, note = classify_failure(log_text, exit_code, row["recipe_class"])
            row["failure_type"] = failure_type
            row["notes"] = (row.get("notes", "") + f";{note}").strip(";")
            if failure_type in {"missing_pool", "missing_relation_match"}:
                row["status"] = "partial_complete"
                row["queue_name"] = "done"
                break
            if retryable and row["retry_count"] < MAX_RETRIES:
                row["retry_count"] += 1
                row["queue_name"] = "retry_queue"
                row["status"] = "retry_wait"
                row["next_retry_at"] = datetime.fromtimestamp(utc_epoch() + 10, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            elif failure_type == "oom":
                row["status"] = "blocked"
                row["queue_name"] = "blocked"
            elif failure_type == "code_error":
                row["status"] = "failed_permanent"
                row["queue_name"] = "blocked"
            else:
                row["status"] = "blocked" if row["recipe_class"] == "runtime_unverified" else "failed_permanent"
                row["queue_name"] = "blocked"
            break


def launch_job(job: dict[str, Any], gpu: str) -> None:
    config_path = ROOT / job["config_path"]
    log_path = ROOT / job["log_path"]
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.pop("LD_LIBRARY_PATH", None)
    gpu_id = visible_devices(job, gpu)
    env["CUDA_VISIBLE_DEVICES"] = gpu_id
    env["PYTHONNOUSERSITE"] = "1"
    pair_handle = None
    if job["recipe_class"] == "needs_tp2":
        pair_handle = try_acquire_pair67()
        if pair_handle is None:
            with LockedState() as state:
                for row in state["jobs"]:
                    if row["job_id"] == job["job_id"]:
                        row["status"] = "queued"
                        row["gpu_id"] = ""
                        row["started_at"] = ""
                        row["notes"] = (row.get("notes", "") + ";waiting_for_tp2_pair").strip(";")
                        break
            return
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[worker] {utc_now()} start job_id={job['job_id']} gpu={gpu_id} cfg={job['config_path']}\n")
        handle.flush()
        process = subprocess.Popen(
            [str(PYTHON), "-u", "-m", "crb_v2.cli", "--config", str(config_path)],
            cwd=ROOT,
            stdout=handle,
            stderr=subprocess.STDOUT,
            env=env,
        )
        mark_running(job["job_id"], gpu_id, process.pid)
        exit_code = process.wait()
        handle.write(f"[worker] {utc_now()} finish job_id={job['job_id']} gpu={gpu_id} exit={exit_code}\n")
        handle.flush()
    release_pair67(pair_handle)
    finalize_job(job, exit_code, gpu_id)


def write_worker_state(gpu: str, lane: str, pid: int, status: str) -> None:
    ensure_dirs()
    if WORKER_STATE_PATH.exists():
        payload = json.loads(WORKER_STATE_PATH.read_text(encoding="utf-8"))
    else:
        payload = {}
    payload[gpu] = {"lane": lane, "pid": pid, "status": status, "updated_at": utc_now()}
    write_json(WORKER_STATE_PATH, payload)


def worker_loop(gpu: str, lane: str) -> None:
    ensure_dirs()
    write_worker_state(gpu, lane, os.getpid(), "running")
    last_refresh = 0.0
    while True:
        if gpu == "7" and utc_epoch() - last_refresh > SUMMARY_REFRESH_SECONDS:
            refresh_external_inventory()
            last_refresh = utc_epoch()
        job = claim_job(gpu)
        if job is None:
            time.sleep(IDLE_SLEEP_SECONDS)
            continue
        launch_job(job, gpu)
        if gpu == "7":
            refresh_external_inventory()


def start_workers() -> None:
    ensure_dirs()
    workers = [
        ("4", "main_bulk_lane_a"),
        ("5", "main_bulk_lane_b"),
        ("6", "probation_retry_lane"),
    ]
    pids = []
    for index, (gpu, lane) in enumerate(workers):
        log_path = WORKER_LOG_DIR / f"gpu{gpu}_worker.log"
        with log_path.open("a", encoding="utf-8") as handle:
            process = subprocess.Popen(
                [str(PYTHON), "-u", str(ROOT / "tools" / "crb_v2_bulk_supervisor.py"), "worker", "--gpu", gpu, "--lane", lane],
                cwd=ROOT,
                stdout=handle,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                env=os.environ.copy(),
                start_new_session=True,
            )
        pids.append({"gpu": gpu, "lane": lane, "pid": process.pid, "log_path": str(log_path.relative_to(ROOT))})
        write_worker_state(gpu, lane, process.pid, "running")
        if index < len(workers) - 1:
            time.sleep(10)
    write_json(STATUS_DIR / "launched_workers.json", pids)
    print(json.dumps(pids, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="CRB v2 bulk supervisor")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("start")
    sub.add_parser("launch-workers")
    worker_parser = sub.add_parser("worker")
    worker_parser.add_argument("--gpu", required=True)
    worker_parser.add_argument("--lane", required=True)
    sub.add_parser("refresh")
    args = parser.parse_args()

    if args.cmd == "init":
        init_state()
    elif args.cmd == "refresh":
        with LockedState() as state:
            reconcile_stale_jobs(state)
        refresh_external_inventory()
    elif args.cmd == "start":
        init_state()
        start_workers()
    elif args.cmd == "launch-workers":
        start_workers()
    elif args.cmd == "worker":
        worker_loop(args.gpu, args.lane)


if __name__ == "__main__":
    main()
