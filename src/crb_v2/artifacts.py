from __future__ import annotations

from pathlib import Path

from crb_v2.config import PipelineConfig
from crb_v2.types import to_dict
from crb_v2.utils import stable_hash



def experiment_root(config: PipelineConfig) -> Path:
    signature = stable_hash(to_dict(config), length=16)
    return Path(config.output.root_dir) / f"{config.experiment_name}__{signature}"



def baseline_dir(root: Path, model_key: str, benchmark_key: str) -> Path:
    return root / "baseline" / model_key / benchmark_key



def pool_dir(root: Path, model_key: str, benchmark_key: str) -> Path:
    return root / "pools" / model_key / benchmark_key



def sweep_dir(root: Path, model_key: str, benchmark_key: str, relation: str, provenance: str, k: int) -> Path:
    return root / "sweep" / model_key / benchmark_key / relation / provenance / f"k_{k}"



def aggregate_dir(root: Path) -> Path:
    return root / "aggregate"
