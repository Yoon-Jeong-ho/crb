from __future__ import annotations

from pathlib import Path

from crb.schemas import RunConfig, dataclass_to_dict
from crb.utils.hashing import stable_hash



def config_hash(config: RunConfig) -> str:
    return stable_hash(config.to_dict(), length=16)



def run_root(config: RunConfig) -> Path:
    signature = config_hash(config)
    return Path(config.runtime.output_root) / "runs" / f"{config.experiment.name}__{signature}"



def manifest_path(config: RunConfig) -> Path:
    signature = stable_hash(
        {
            "seed": config.experiment.seed,
            "ks": config.evaluation.manifest_k_values,
            "dummy_type": config.evaluation.dummy_type,
            "target": dataclass_to_dict(config.evaluation.target),
            "dummy_sources": dataclass_to_dict(config.evaluation.dummy_sources),
        },
        length=16,
    )
    return (
        Path(config.runtime.manifest_dir)
        / f"{config.experiment.name}__manifest__{signature}.json"
    )
