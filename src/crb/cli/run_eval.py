from __future__ import annotations

import argparse
import json

from crb.evaluation.runner import run_from_config



def main() -> None:
    parser = argparse.ArgumentParser(description="Run a CRB evaluation config")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    args = parser.parse_args()
    result = run_from_config(args.config)
    print(json.dumps({"run_id": result["run_id"], "metrics": result["metrics"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
