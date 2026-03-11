from __future__ import annotations

import argparse
import copy
import itertools
from pathlib import Path
from typing import Any

import yaml


def _set_nested(mapping: dict[str, Any], dotted_key: str, value: Any) -> None:
    current = mapping
    parts = dotted_key.split(".")
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _slugify(value: Any) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace("/", "-")
        .replace(" ", "_")
        .replace(".", "p")
    )


def materialize_sweep(spec_path: Path) -> list[Path]:
    spec = _load_yaml(spec_path)
    output_dir = Path(spec["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    presets = spec.get("presets", {})
    generated_paths: list[Path] = []

    for job in spec["jobs"]:
        base_config = _load_yaml(Path(job["base_config"]))
        matrix = job.get("matrix", {})
        axes = list(matrix.keys())
        values = [matrix[axis] for axis in axes]
        variants = job.get("variants", [None])
        for variant_name in variants:
            variant_overrides = presets.get(variant_name, {}) if variant_name else {}
            for combo in itertools.product(*values):
                rendered = copy.deepcopy(base_config)
                suffix_parts: list[str] = [job["name"]]
                if variant_name:
                    suffix_parts.append(_slugify(variant_name))
                for dotted_key, value in variant_overrides.items():
                    _set_nested(rendered, dotted_key, value)
                for dotted_key, value in zip(axes, combo, strict=True):
                    _set_nested(rendered, dotted_key, value)
                    suffix_parts.append(f"{dotted_key.split('.')[-1]}-{_slugify(value)}")

                experiment_name = rendered["experiment"]["name"]
                rendered["experiment"]["name"] = f"{experiment_name}__{'__'.join(suffix_parts[1:])}"
                file_name = f"{'__'.join(suffix_parts)}.yaml"
                output_path = output_dir / file_name
                with output_path.open("w", encoding="utf-8") as handle:
                    yaml.safe_dump(rendered, handle, sort_keys=False, allow_unicode=True)
                generated_paths.append(output_path)

    manifest_path = output_dir / "_generated_files.txt"
    with manifest_path.open("w", encoding="utf-8") as handle:
        for generated_path in generated_paths:
            handle.write(f"{generated_path}\n")
    return generated_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize CRB sweep YAML specs into concrete configs")
    parser.add_argument("--spec", required=True, help="Path to sweep spec YAML")
    args = parser.parse_args()
    generated = materialize_sweep(Path(args.spec))
    print(f"generated {len(generated)} configs")
    if generated:
        print(generated[0])


if __name__ == "__main__":
    main()
