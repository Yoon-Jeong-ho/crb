from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path


def utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def resolve_tensor_parallel_size(value: int | str) -> int:
    if isinstance(value, int):
        return value
    visible = os.environ.get("CUDA_VISIBLE_DEVICES", "")
    if not visible:
        return 1
    device_ids = [item.strip() for item in visible.split(",") if item.strip()]
    return max(1, len(device_ids))


def ensure_parent(path: str | Path) -> Path:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved
