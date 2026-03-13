from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

SCOREBOARD = Path('results/summary/scoreboard.csv')
ANALYSIS_DIR = Path('results/analysis')
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
EXCLUDE_PATH_TOKENS = ['strictfinal', 'multigpu', 'smoke', 'choiceconstrained']
MAIN_TABLE_CONDITIONS = [
    {
        'dataset': 'mmlu',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'k': '2',
    },
    {
        'dataset': 'gsm8k',
        'evaluation_mode': 'single_turn_flattened',
        'history_mode': 'self_history',
        'dummy_type': 'cross_domain',
        'k': '2',
    },
    {
        'dataset': 'gpqa',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'k': '2',
    },
    {
        'dataset': 'aime',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'k': '2',
    },
]


def load_rows() -> list[dict[str, str]]:
    with SCOREBOARD.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def is_canonical(row: dict[str, str]) -> bool:
    result_path = row.get('result_json_path', '')
    return not any(token in result_path for token in EXCLUDE_PATH_TOKENS)


def latest_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    latest: dict[tuple[str, str, str, str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (
            row.get('model_name', ''),
            row.get('thinking_mode', ''),
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
            row.get('k', ''),
        )
        latest[key] = row
    return list(latest.values())


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_direct_pairs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str, str, str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        key = (
            row.get('model_name', ''),
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
            row.get('k', ''),
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
                    'k': key[5],
                    'off_run_id': off['run_id'],
                    'on_run_id': on['run_id'],
                    'off_num_items': off['num_items'],
                    'on_num_items': on['num_items'],
                    'off_accuracy': off['accuracy'],
                    'on_accuracy': on['accuracy'],
                    'off_format_failure_rate': off['format_failure_rate'],
                    'on_format_failure_rate': on['format_failure_rate'],
                }
            )
    return pairs


def build_main_table(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    allowed = {
        (
            condition['dataset'],
            condition['evaluation_mode'],
            condition['history_mode'],
            condition['dummy_type'],
            condition['k'],
        )
        for condition in MAIN_TABLE_CONDITIONS
    }
    direct_pairs = build_direct_pairs(rows)
    return [
        row
        for row in direct_pairs
        if (
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
            row.get('k', ''),
        )
        in allowed
    ]


def main() -> None:
    rows = load_rows()
    qwen3_rows = [row for row in rows if row.get('model_family') == 'qwen3']
    latest_all = latest_rows(qwen3_rows)
    latest_canonical = latest_rows([row for row in qwen3_rows if is_canonical(row)])

    latest_sorted = sorted(
        latest_all,
        key=lambda row: (
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
            row.get('k', ''),
            row.get('thinking_mode', ''),
            row.get('run_id', ''),
        ),
    )
    latest_canonical_sorted = sorted(
        latest_canonical,
        key=lambda row: (
            row.get('dataset', ''),
            row.get('evaluation_mode', ''),
            row.get('history_mode', ''),
            row.get('dummy_type', ''),
            row.get('k', ''),
            row.get('thinking_mode', ''),
            row.get('run_id', ''),
        ),
    )

    write_csv(ANALYSIS_DIR / 'latest_qwen3_runs.csv', latest_sorted, list(latest_sorted[0].keys()) if latest_sorted else [])
    write_csv(ANALYSIS_DIR / 'latest_qwen3_runs_canonical.csv', latest_canonical_sorted, list(latest_canonical_sorted[0].keys()) if latest_canonical_sorted else [])

    pairs = build_direct_pairs(latest_canonical_sorted)
    pair_fields = [
        'model_name', 'dataset', 'evaluation_mode', 'history_mode', 'dummy_type', 'k',
        'off_run_id', 'on_run_id', 'off_num_items', 'on_num_items',
        'off_accuracy', 'on_accuracy',
        'off_format_failure_rate', 'on_format_failure_rate',
    ]
    write_csv(ANALYSIS_DIR / 'direct_qwen3_pairs.csv', pairs, pair_fields)
    with (ANALYSIS_DIR / 'direct_qwen3_pairs.json').open('w', encoding='utf-8') as handle:
        json.dump(pairs, handle, ensure_ascii=False, indent=2)

    main_table = build_main_table(latest_canonical_sorted)
    write_csv(ANALYSIS_DIR / 'main_table_qwen3.csv', main_table, pair_fields)
    with (ANALYSIS_DIR / 'main_table_qwen3.json').open('w', encoding='utf-8') as handle:
        json.dump(main_table, handle, ensure_ascii=False, indent=2)

    summary = {
        'qwen3_total_rows': len(qwen3_rows),
        'qwen3_latest_condition_rows': len(latest_sorted),
        'qwen3_latest_canonical_condition_rows': len(latest_canonical_sorted),
        'direct_pair_count': len(pairs),
        'main_table_row_count': len(main_table),
        'datasets': sorted({row.get('dataset', '') for row in latest_sorted}),
        'excluded_noncanonical_tokens': EXCLUDE_PATH_TOKENS,
    }
    with (ANALYSIS_DIR / 'summary_overview.json').open('w', encoding='utf-8') as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
