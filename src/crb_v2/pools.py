from __future__ import annotations

from pathlib import Path

from crb_v2.artifacts import baseline_dir, pool_dir
from crb_v2.benchmarks import create_adapter
from crb_v2.config import ModelConfig, PipelineConfig
from crb_v2.io import read_jsonl, write_json
from crb_v2.types import ManifestEntry, to_dict
from crb_v2.utils import stable_hash



def build_pools_for_model(*, config: PipelineConfig, experiment_root: Path, model: ModelConfig) -> dict[str, dict]:
    benchmark_domains: dict[str, str] = {}
    source_rows: dict[str, dict[str, list[dict]]] = {}
    oracle_rows: dict[str, list[dict]] = {}
    for benchmark in config.benchmarks:
        adapter = create_adapter(benchmark)
        benchmark_domains[benchmark.key] = adapter.benchmark_domain()
        base_dir = baseline_dir(experiment_root, model.key, benchmark.key)
        source_rows[benchmark.key] = {
            "model_correct": read_jsonl(base_dir / "correct_pool.jsonl"),
            "model_incorrect": read_jsonl(base_dir / "incorrect_pool.jsonl"),
        }
        oracle_rows[benchmark.key] = read_jsonl(base_dir / "oracle_pool.jsonl")

    summaries: dict[str, dict] = {}
    max_k = max(config.sweep.k_values)
    for target_benchmark in config.benchmarks:
        target_results = read_jsonl(baseline_dir(experiment_root, model.key, target_benchmark.key) / "items.jsonl")
        out_dir = pool_dir(experiment_root, model.key, target_benchmark.key)
        relation_payload: dict[str, dict] = {}
        for relation in config.sweep.relations:
            for provenance in config.sweep.provenances:
                entries = []
                for target in target_results:
                    candidates = _relation_candidates(
                        target=target,
                        target_benchmark=target_benchmark.key,
                        relation=relation,
                        provenance=provenance,
                        benchmark_domains=benchmark_domains,
                        source_rows=source_rows,
                        oracle_rows=oracle_rows,
                    )
                    ordered = sorted(
                        candidates,
                        key=lambda row: stable_hash(
                            {
                                "seed": config.runtime.seed,
                                "target": target["example_id"],
                                "relation": relation,
                                "provenance": provenance,
                                "source": row["example_id"],
                                "source_benchmark": row["benchmark_name"],
                            },
                            length=32,
                        ),
                    )
                    entries.append(
                        ManifestEntry(
                            target_example_id=target["example_id"],
                            relation=relation,
                            provenance=provenance,
                            ordered_dummy_ids=[row["example_id"] for row in ordered[:max_k]],
                            ordered_dummy_benchmarks=[row["benchmark_name"] for row in ordered[:max_k]],
                        )
                    )
                manifest_path = out_dir / relation / f"{provenance}.json"
                write_json(
                    manifest_path,
                    {
                        "model_key": model.key,
                        "target_benchmark": target_benchmark.key,
                        "relation": relation,
                        "provenance": provenance,
                        "max_k": max_k,
                        "entries": [to_dict(entry) for entry in entries],
                    },
                )
                relation_payload[f"{relation}:{provenance}"] = {
                    "entry_count": len(entries),
                    "min_candidate_count": min((len(entry.ordered_dummy_ids) for entry in entries), default=0),
                    "max_candidate_count": max((len(entry.ordered_dummy_ids) for entry in entries), default=0),
                    "manifest_path": str(manifest_path),
                }
        write_json(out_dir / "summary.json", {"target_benchmark": target_benchmark.key, "relations": relation_payload})
        summaries[target_benchmark.key] = {"target_benchmark": target_benchmark.key, "relations": relation_payload}
    return summaries



def _relation_candidates(*, target: dict, target_benchmark: str, relation: str, provenance: str, benchmark_domains: dict[str, str], source_rows: dict[str, dict[str, list[dict]]], oracle_rows: dict[str, list[dict]]) -> list[dict]:
    candidates: list[dict] = []
    target_domain = benchmark_domains[target_benchmark]
    for source_benchmark, source_domain in benchmark_domains.items():
        if relation == "same_benchmark" and source_benchmark != target_benchmark:
            continue
        if relation == "same_domain_other_benchmark" and (source_benchmark == target_benchmark or source_domain != target_domain):
            continue
        if relation == "cross_domain" and source_domain == target_domain:
            continue
        bucket = oracle_rows[source_benchmark] if provenance == "oracle" else source_rows[source_benchmark][provenance]
        for row in bucket:
            if source_benchmark == target_benchmark and row["example_id"] == target["example_id"]:
                continue
            if row.get("question", "").strip() == target.get("metadata", {}).get("question", "").strip():
                continue
            candidates.append(row)
    return candidates
