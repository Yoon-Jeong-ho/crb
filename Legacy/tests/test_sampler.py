from pathlib import Path

from crb.config import load_run_config
from crb.datasets import load_items
from crb.datasets import hf_loaders  # noqa: F401
from crb.evaluation.runner import _load_dummy_items, _prepare_items
from crb.sampling.dummy_sampler import build_or_load_manifest


def test_manifest_generation(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_multiturn_oracle.yaml")
    config.runtime.manifest_dir = str(tmp_path / "manifests")
    target_items = _prepare_items(load_items(config.evaluation.target), config.evaluation.target, config.experiment.num_samples)
    dummy_items = _load_dummy_items(config)
    manifest, path, created = build_or_load_manifest(config=config, target_items=target_items, dummy_items=dummy_items)
    assert created is True
    assert path.exists()
    assert len(manifest.entries) == 2
    assert len(manifest.entries[0].dummy_ids_by_type["same_domain"]) == 2
