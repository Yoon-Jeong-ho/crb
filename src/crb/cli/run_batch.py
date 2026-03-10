from __future__ import annotations

import argparse
import json
from pathlib import Path

from crb.evaluation.runner import run_from_config



def main() -> None:
    parser = argparse.ArgumentParser(description="Run multiple CRB configs sequentially")
    parser.add_argument("configs", nargs="+", help="Config files or directories")
    args = parser.parse_args()

    config_paths: list[Path] = []
    for token in args.configs:
        path = Path(token)
        if path.is_dir():
            config_paths.extend(sorted(path.glob("*.yaml")))
            config_paths.extend(sorted(path.glob("*.yml")))
        else:
            config_paths.append(path)

    results = [run_from_config(path) for path in config_paths]
    print(json.dumps([{"config": str(path), "run_id": result["run_id"]} for path, result in zip(config_paths, results)], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
