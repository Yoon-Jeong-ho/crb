from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = REPO_ROOT / "Legacy"
SCOREBOARD_PATH = LEGACY_ROOT / "results" / "summary" / "scoreboard.csv"
ANALYSIS_ROOT = REPO_ROOT / "analysis"


def read_scoreboard_rows(path: Path = SCOREBOARD_PATH) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_run_payload(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_load_run_payload(path: str | Path) -> dict[str, Any] | None:
    target = Path(path)
    if not target.exists():
        return None
    return json.loads(target.read_text(encoding="utf-8"))


def _extract_json_object(text: str, anchor: str) -> dict[str, Any] | None:
    start = text.find(anchor)
    if start == -1:
        return None
    brace_start = text.find("{", start)
    if brace_start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for idx in range(brace_start, len(text)):
        ch = text[idx]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[brace_start : idx + 1])
                except json.JSONDecodeError:
                    return None
    return None


def load_run_payload_summary(path: str | Path) -> dict[str, Any] | None:
    target = Path(path)
    if not target.exists():
        return None
    with target.open("r", encoding="utf-8") as handle:
        text = handle.read(65536)
    manifest_match = re.search(r'"manifest_path"\s*:\s*"([^"]*)"', text)
    metrics = _extract_json_object(text, '"metrics"') or {}
    if not metrics or not manifest_match:
        text = target.read_text(encoding="utf-8")
        manifest_match = manifest_match or re.search(r'"manifest_path"\s*:\s*"([^"]*)"', text)
        metrics = metrics or (_extract_json_object(text, '"metrics"') or {})
    return {
        "manifest_path": manifest_match.group(1) if manifest_match else "",
        "metrics": metrics,
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_markdown_table(path: Path, title: str, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    if not rows:
        lines.append("_No rows matched the requested slice._")
    else:
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def normalize_int(value: str | int | None) -> int:
    if value in (None, ""):
        return 0
    return int(value)


def normalize_float(value: str | float | int | None) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)
