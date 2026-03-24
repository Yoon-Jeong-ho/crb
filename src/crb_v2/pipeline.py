from __future__ import annotations

from pathlib import Path

from crb_v2.aggregate import aggregate_results
from crb_v2.artifacts import experiment_root
from crb_v2.baseline import run_baseline_for_model
from crb_v2.config import PipelineConfig, load_pipeline_config
from crb_v2.engines.factory import create_engine, resolve_model_config
from crb_v2.io import write_json
from crb_v2.pools import build_pools_for_model
from crb_v2.sweep import run_sweeps_for_model
from crb_v2.types import to_dict



def run_pipeline(config_or_path: PipelineConfig | str | Path) -> dict:
    config = load_pipeline_config(config_or_path) if not isinstance(config_or_path, PipelineConfig) else config_or_path
    root = experiment_root(config)
    root.mkdir(parents=True, exist_ok=True)
    write_json(root / "resolved_config.json", to_dict(config))

    baseline_summaries = {}
    pool_summaries = {}
    sweep_summaries = {}
    for model in config.models:
        model = resolve_model_config(model)
        baseline_engine = create_engine(model)
        try:
            baseline_summaries[model.key] = run_baseline_for_model(config=config, experiment_root=root, model=model, engine=baseline_engine)
        finally:
            baseline_engine.close()
        pool_summaries[model.key] = build_pools_for_model(config=config, experiment_root=root, model=model)
        sweep_engine = create_engine(model)
        try:
            sweep_summaries[model.key] = run_sweeps_for_model(config=config, experiment_root=root, model=model, engine=sweep_engine)
        finally:
            sweep_engine.close()
    aggregate_paths = aggregate_results(config=config, experiment_root=root)
    payload = {
        "experiment_root": str(root),
        "baseline_summaries": baseline_summaries,
        "pool_summaries": pool_summaries,
        "sweep_summaries": sweep_summaries,
        "aggregate_paths": aggregate_paths,
    }
    write_json(root / "pipeline_result.json", payload)
    return payload
