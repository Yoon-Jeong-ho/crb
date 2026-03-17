from __future__ import annotations

import json
import random
from pathlib import Path

from crb.schemas import EvaluationManifest, ManifestEntry, NormalizedItem, RunConfig, dataclass_to_dict
from crb.utils.hashing import stable_hash
from crb.utils.paths import manifest_path
from crb.utils.runtime import utc_timestamp


class ManifestError(ValueError):
    """Raised when a reproducible dummy-pack manifest cannot be produced."""



def build_or_load_manifest(
    *,
    config: RunConfig,
    target_items: list[NormalizedItem],
    dummy_items: list[NormalizedItem],
) -> tuple[EvaluationManifest, Path, bool]:
    path = manifest_path(config)
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        manifest = EvaluationManifest(
            manifest_id=payload["manifest_id"],
            config_hash=payload["config_hash"],
            seed=payload["seed"],
            ks=payload["ks"],
            target_sources=payload["target_sources"],
            dummy_sources=payload["dummy_sources"],
            entries=[ManifestEntry(**entry) for entry in payload["entries"]],
        )
        return manifest, path, False

    requested_modes = [config.evaluation.dummy_type]
    max_k = max(config.evaluation.manifest_k_values)
    entries: list[ManifestEntry] = []
    for target in target_items:
        dummy_ids_by_type: dict[str, list[str]] = {}
        for mode in requested_modes:
            dummy_ids_by_type[mode] = _sample_candidates(
                target=target,
                dummy_items=dummy_items,
                seed=config.experiment.seed,
                max_k=max_k,
                mode=mode,
            )
        entries.append(
            ManifestEntry(
                target_item_id=target.item_id,
                target_dataset_name=target.dataset_name,
                target_subject=target.subject,
                target_domain=target.domain,
                dummy_ids_by_type=dummy_ids_by_type,
            )
        )

    manifest = EvaluationManifest(
        manifest_id=f"manifest-{utc_timestamp()}",
        config_hash=stable_hash(config.to_dict(), length=16),
        seed=config.experiment.seed,
        ks=sorted(config.evaluation.manifest_k_values),
        target_sources=[dataclass_to_dict(config.evaluation.target)],
        dummy_sources=[dataclass_to_dict(source) for source in (config.evaluation.dummy_sources or [config.evaluation.target])],
        entries=entries,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(manifest.to_dict(), handle, ensure_ascii=False, indent=2)
    return manifest, path, True



def _sample_candidates(
    *,
    target: NormalizedItem,
    dummy_items: list[NormalizedItem],
    seed: int,
    max_k: int,
    mode: str,
) -> list[str]:
    if max_k == 0:
        return []
    candidates: list[NormalizedItem] = []
    for candidate in dummy_items:
        if candidate.item_id == target.item_id and candidate.dataset_name == target.dataset_name:
            continue
        if candidate.question.strip() == target.question.strip():
            continue
        if _matches_mode(target, candidate, mode):
            candidates.append(candidate)
    if len(candidates) < max_k:
        raise ManifestError(
            f"Not enough `{mode}` dummy candidates for target {target.item_id}: "
            f"need {max_k}, found {len(candidates)}"
        )
    shuffle_seed = stable_hash(
        {"seed": seed, "target_item_id": target.item_id, "mode": mode}, length=32
    )
    rng = random.Random(int(shuffle_seed, 16))
    candidate_ids = [item.item_id for item in candidates]
    rng.shuffle(candidate_ids)
    return candidate_ids[:max_k]



def _matches_mode(target: NormalizedItem, candidate: NormalizedItem, mode: str) -> bool:
    same_subject = bool(
        target.subject and candidate.subject and target.subject.strip().lower() == candidate.subject.strip().lower()
    )
    same_domain = bool(
        target.domain and candidate.domain and target.domain.strip().lower() == candidate.domain.strip().lower()
    )
    different_dataset = target.dataset_name != candidate.dataset_name
    if mode == "same_domain":
        if target.subject or candidate.subject or target.domain or candidate.domain:
            return same_subject or same_domain
        return target.dataset_name == candidate.dataset_name
    if mode == "same_domain_other_dataset":
        if target.subject or candidate.subject or target.domain or candidate.domain:
            return different_dataset and (same_subject or same_domain)
        return False
    if mode == "cross_domain":
        if target.subject or candidate.subject or target.domain or candidate.domain:
            return not (same_subject or same_domain)
        return target.dataset_name != candidate.dataset_name
    raise ValueError(f"Unknown mode: {mode}")



def manifest_entry_lookup(manifest: EvaluationManifest) -> dict[str, ManifestEntry]:
    return {entry.target_item_id: entry for entry in manifest.entries}
