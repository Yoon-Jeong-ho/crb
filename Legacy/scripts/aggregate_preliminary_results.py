from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

SCOREBOARD = Path('results/summary/scoreboard.csv')
ANALYSIS_DIR = Path('results/analysis')
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
EXCLUDE_PATH_TOKENS = ['strictfinal', 'multigpu_smoke']


def load_rows() -> list[dict[str, str]]:
    with SCOREBOARD.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def is_canonical(row: dict[str, str]) -> bool:
    result_path = row.get('result_json_path', '')
    return not any(token in result_path for token in EXCLUDE_PATH_TOKENS)


def latest_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    latest: dict[tuple[str, str, str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (
            row.get('model_name', ''),
            row.get('thinking_mode', ''),
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
        )
        latest[key] = row
    return list(latest.values())


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_direct_pairs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str, str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        key = (
            row.get('model_name', ''),
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
        )
        grouped[key][row.get('thinking_mode', '')] = row

    pairs: list[dict[str, str]] = []
    for key, modes in grouped.items():
        if 'off' in modes and 'on' in modes:
            off = modes['off']
            on = modes['on']
            pairs.append(
                {
                    'model_name': key[0],
                    'dataset': key[1],
                    'evaluation_mode': key[2],
                    'history_mode': key[3],
                    'dummy_type': key[4],
                    'off_run_id': off['run_id'],
                    'on_run_id': on['run_id'],
                    'off_accuracy': off['accuracy'],
                    'on_accuracy': on['accuracy'],
                    'off_format_failure_rate': off['format_failure_rate'],
                    'on_format_failure_rate': on['format_failure_rate'],
                }
            )
    return pairs


def main() -> None:
    rows = load_rows()
    qwen3_rows = [row for row in rows if row.get('model_family') == 'qwen3']
    latest_all = latest_rows(qwen3_rows)
    latest_canonical = latest_rows([row for row in qwen3_rows if is_canonical(row)])

    latest_sorted = sorted(
        latest_all,
        key=lambda row: (row.get('dataset', ''), row.get('evaluation_mode', ''), row.get('history_mode', ''), row.get('thinking_mode', ''), row.get('run_id', '')),
    )
    latest_canonical_sorted = sorted(
        latest_canonical,
        key=lambda row: (row.get('dataset', ''), row.get('evaluation_mode', ''), row.get('history_mode', ''), row.get('thinking_mode', ''), row.get('run_id', '')),
    )

    write_csv(ANALYSIS_DIR / 'latest_qwen3_runs.csv', latest_sorted, list(latest_sorted[0].keys()) if latest_sorted else [])
    write_csv(ANALYSIS_DIR / 'latest_qwen3_runs_canonical.csv', latest_canonical_sorted, list(latest_canonical_sorted[0].keys()) if latest_canonical_sorted else [])

    pairs = build_direct_pairs(latest_canonical_sorted)
    pair_fields = [
        'model_name', 'dataset', 'evaluation_mode', 'history_mode', 'dummy_type',
        'off_run_id', 'on_run_id', 'off_accuracy', 'on_accuracy',
        'off_format_failure_rate', 'on_format_failure_rate',
    ]
    write_csv(ANALYSIS_DIR / 'direct_qwen3_pairs.csv', pairs, pair_fields)
    with (ANALYSIS_DIR / 'direct_qwen3_pairs.json').open('w', encoding='utf-8') as handle:
        json.dump(pairs, handle, ensure_ascii=False, indent=2)

    summary = {
        'qwen3_total_rows': len(qwen3_rows),
        'qwen3_latest_condition_rows': len(latest_sorted),
        'qwen3_latest_canonical_condition_rows': len(latest_canonical_sorted),
        'direct_pair_count': len(pairs),
        'datasets': sorted({row.get('dataset', '') for row in latest_sorted}),
        'excluded_noncanonical_tokens': EXCLUDE_PATH_TOKENS,
    }
    with (ANALYSIS_DIR / 'summary_overview.json').open('w', encoding='utf-8') as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
