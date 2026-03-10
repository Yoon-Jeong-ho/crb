from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from crb.utils.runtime import ensure_parent


SCOREBOARD_COLUMNS = [
    "timestamp",
    "run_id",
    "git_commit",
    "model_name",
    "dataset",
    "split",
    "evaluation_mode",
    "history_mode",
    "dummy_type",
    "k",
    "seed",
    "num_items",
    "accuracy",
    "format_failure_rate",
    "result_json_path",
]



def append_jsonl(path: str | Path, record: dict[str, Any]) -> None:
    target = ensure_parent(path)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")



def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    target = Path(path)
    if not target.exists():
        return []
    records: list[dict[str, Any]] = []
    with target.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records



def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = ensure_parent(path)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)



def append_scoreboard(path: str | Path, row: dict[str, Any]) -> None:
    target = ensure_parent(path)
    file_exists = target.exists()
    with target.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCOREBOARD_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({column: row.get(column, "") for column in SCOREBOARD_COLUMNS})
