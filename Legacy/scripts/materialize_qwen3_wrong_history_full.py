from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "configs/generated/qwen3_wrong_history_full"


def materialize() -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    template = yaml.safe_load((ROOT / "configs/templates/qwen3_1p7b_gpqa_base.yaml").read_text(encoding="utf-8"))
    created: list[Path] = []

    for k in (2, 4, 8):
        config = deepcopy(template)
        config["experiment"]["name"] = f"qwen3_1p7b_gpqa_wrong_history_same_domain_full_k{k}"
        config["experiment"]["num_samples"] = None
        tags = list(config["experiment"].get("tags", []))
        tags.extend(["wrong_history", "full_samples", "same_domain", f"k{k}"])
        config["experiment"]["tags"] = tags

        config["model"]["thinking_mode"] = "off"
        config["model"]["chat_template_kwargs"]["enable_thinking"] = False
        config["decoding"]["temperature"] = 0.7
        config["decoding"]["top_p"] = 0.8
        config["decoding"]["top_k"] = 20
        config["decoding"]["max_tokens"] = 1024

        config["evaluation"]["evaluation_mode"] = "multi_turn"
        config["evaluation"]["history_mode"] = "wrong_history"
        config["evaluation"]["dummy_type"] = "same_domain"
        config["evaluation"]["k"] = k

        out = OUTPUT_DIR / f"qwen3_gpqa_wrong_history_same_domain__k-{k}.yaml"
        out.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
        created.append(out)

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
