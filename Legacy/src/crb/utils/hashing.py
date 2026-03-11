from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_hash(payload: Any, *, length: int = 12) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:length]
