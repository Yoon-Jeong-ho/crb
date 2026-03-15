from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "configs/generated/qwen3_gpqa_cross_domain_full"


def make_base() -> dict:
    return yaml.safe_load((ROOT / "configs/templates/qwen3_1p7b_gpqa_base.yaml").read_text(encoding="utf-8"))


def configure_off(config: dict) -> None:
    config["model"]["thinking_mode"] = "off"
    config["model"]["chat_template_kwargs"]["enable_thinking"] = False
    config["decoding"]["temperature"] = 0.7
    config["decoding"]["top_p"] = 0.8
    config["decoding"]["top_k"] = 20
    config["decoding"]["max_tokens"] = 1024


def materialize() -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for k in (2, 4, 8):
        off_cfg = deepcopy(make_base())
        off_cfg["experiment"]["name"] = f"qwen3_1p7b_gpqa_cross_domain_oracle_full_k{k}"
        off_cfg["experiment"]["num_samples"] = None
        off_cfg["experiment"]["tags"] = list(off_cfg["experiment"].get("tags", [])) + [
            "cross_domain",
            "oracle_history",
            "full_samples",
            f"k{k}",
        ]
        configure_off(off_cfg)
        off_cfg["evaluation"]["evaluation_mode"] = "multi_turn"
        off_cfg["evaluation"]["history_mode"] = "oracle_history"
        off_cfg["evaluation"]["dummy_type"] = "cross_domain"
        off_cfg["evaluation"]["k"] = k
        off_out = OUTPUT_DIR / f"gpqa_cross_domain_oracle__k-{k}.yaml"
        off_out.write_text(yaml.safe_dump(off_cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
        created.append(off_out)

        wrong_cfg = deepcopy(make_base())
        wrong_cfg["experiment"]["name"] = f"qwen3_1p7b_gpqa_cross_domain_wrong_full_k{k}"
        wrong_cfg["experiment"]["num_samples"] = None
        wrong_cfg["experiment"]["tags"] = list(wrong_cfg["experiment"].get("tags", [])) + [
            "cross_domain",
            "wrong_history",
            "full_samples",
            f"k{k}",
        ]
        configure_off(wrong_cfg)
        wrong_cfg["evaluation"]["evaluation_mode"] = "multi_turn"
        wrong_cfg["evaluation"]["history_mode"] = "wrong_history"
        wrong_cfg["evaluation"]["dummy_type"] = "cross_domain"
        wrong_cfg["evaluation"]["k"] = k
        wrong_out = OUTPUT_DIR / f"gpqa_cross_domain_wrong__k-{k}.yaml"
        wrong_out.write_text(yaml.safe_dump(wrong_cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
        created.append(wrong_out)

    (OUTPUT_DIR / "_generated_files.txt").write_text(
        "".join(f"{p.relative_to(ROOT)}\n" for p in created),
        encoding="utf-8",
    )
    return created


def main() -> None:
    for path in materialize():
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
