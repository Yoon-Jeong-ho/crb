from pathlib import Path

from crb.config import load_run_config
from crb.datasets import load_items
from crb.datasets import hf_loaders  # noqa: F401
from crb.evaluation.runner import _load_dummy_items, _prepare_items
from crb.schemas import NormalizedItem
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


def test_manifest_only_builds_requested_dummy_type(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_multiturn_oracle.yaml")
    config.runtime.manifest_dir = str(tmp_path / "manifests")
    config.evaluation.dummy_type = "cross_domain"
    target_items = [
        NormalizedItem(
            dataset_name="target",
            split="test",
            item_id="target:test:1",
            domain="math",
            subject="arithmetic",
            question="Q?",
            choices=None,
            answer="1",
            answer_type="numeric",
        )
    ]
    dummy_items = [
        NormalizedItem(
            dataset_name="dummy",
            split="train",
            item_id="dummy:train:1",
            domain="science",
            subject="physics",
            question="D1?",
            choices=["A", "B"],
            answer="A",
            answer_type="mcq",
        ),
        NormalizedItem(
            dataset_name="dummy",
            split="train",
            item_id="dummy:train:2",
            domain="history",
            subject="history",
            question="D2?",
            choices=["A", "B"],
            answer="A",
            answer_type="mcq",
        ),
    ]
    manifest, path, created = build_or_load_manifest(config=config, target_items=target_items, dummy_items=dummy_items)
    assert created is True
    assert path.exists()
    assert sorted(manifest.entries[0].dummy_ids_by_type["cross_domain"]) == [
        "dummy:train:1",
        "dummy:train:2",
    ]
