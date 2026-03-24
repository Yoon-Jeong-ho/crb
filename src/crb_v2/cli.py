from __future__ import annotations

import argparse
import json

from crb_v2.pipeline import run_pipeline



def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CRB v2 integrated pipeline")
    parser.add_argument("--config", required=True, help="Path to a CRB v2 YAML config")
    args = parser.parse_args()
    print(json.dumps(run_pipeline(args.config), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
