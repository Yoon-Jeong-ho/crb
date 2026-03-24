from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any



def stable_hash(payload: Any, *, length: int = 16) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:length]



def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")



def compact_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")



def choose_model_context_limit(value: int | None, tokenizer_limit: int | None) -> int:
    if value:
        return value
    if tokenizer_limit and tokenizer_limit < 1_000_000:
        return int(tokenizer_limit)
    return 8192
