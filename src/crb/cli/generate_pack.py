from __future__ import annotations

import argparse
import json

from crb.config import load_run_config
from crb.datasets import load_items
from crb.datasets import hf_loaders  # noqa: F401  # register HF loaders
from crb.evaluation.runner import _load_dummy_items, _prepare_items
from crb.sampling.dummy_sampler import build_or_load_manifest



def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or reuse a CRB evaluation manifest")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()

    config = load_run_config(args.config)
    target_items = _prepare_items(load_items(config.evaluation.target), config.evaluation.target, config.experiment.num_samples)
    dummy_items = _load_dummy_items(config)
    manifest, path, created = build_or_load_manifest(
        config=config,
        target_items=target_items,
        dummy_items=dummy_items,
    )
    print(json.dumps({"manifest_path": str(path), "created": created, "entries": len(manifest.entries)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
