from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / 'configs/generated/qwen3_main_table_full'

MAIN_TABLE_SPECS = [
    {
        'name': 'mmlu',
        'template': ROOT / 'configs/templates/qwen3_1p7b_mmlu_base.yaml',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'k': 2,
    },
    {
        'name': 'gsm8k',
        'template': ROOT / 'configs/templates/qwen3_1p7b_gsm8k_base.yaml',
        'evaluation_mode': 'single_turn_flattened',
        'history_mode': 'self_history',
        'dummy_type': 'cross_domain',
        'k': 2,
    },
    {
        'name': 'gpqa',
        'template': ROOT / 'configs/templates/qwen3_1p7b_gpqa_base.yaml',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'k': 2,
    },
    {
        'name': 'aime',
        'template': ROOT / 'configs/templates/qwen3_1p7b_aime_base.yaml',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'k': 2,
    },
]

THINKING_VARIANTS = {
    'thinking_off': {
        'model': {
            'thinking_mode': 'off',
            'chat_template_kwargs': {'enable_thinking': False},
        },
        'decoding': {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 20,
            'max_tokens': 1024,
        },
    },
    'thinking_on': {
        'model': {
            'thinking_mode': 'on',
            'chat_template_kwargs': {'enable_thinking': True},
        },
        'decoding': {
            'temperature': 0.6,
            'top_p': 0.95,
            'top_k': 20,
            'max_tokens': 2048,
        },
    },
}


def deep_update(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = deepcopy(value)
    return base


def materialize() -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    for spec in MAIN_TABLE_SPECS:
        base_config = yaml.safe_load(spec['template'].read_text(encoding='utf-8'))
        for variant_name, patch in THINKING_VARIANTS.items():
            config = deepcopy(base_config)
            deep_update(config, patch)

            config['experiment']['num_samples'] = None
            config['experiment']['name'] = (
                f"{config['experiment']['name']}_main_table_full_{variant_name}"
            )
            tags = list(config['experiment'].get('tags', []))
            tags.extend(['main_table', 'full_samples', variant_name])
            if spec['name'] == 'gpqa' and variant_name == 'thinking_on':
                config['prompt']['target_thinking_mode'] = 'no_think'
                config['prompt']['target_response_prefill'] = 'Answer: '
                config['experiment']['name'] += '_nothink_prefill'
                tags.append('gpqa_nothink_prefill')
            config['experiment']['tags'] = tags

            config['evaluation']['evaluation_mode'] = spec['evaluation_mode']
            config['evaluation']['history_mode'] = spec['history_mode']
            config['evaluation']['dummy_type'] = spec['dummy_type']
            config['evaluation']['k'] = spec['k']

            output_path = (
                OUTPUT_DIR
                / f"qwen3_{spec['name']}__{variant_name}__main_table_full.yaml"
            )
            with output_path.open('w', encoding='utf-8') as handle:
                yaml.safe_dump(config, handle, sort_keys=False, allow_unicode=True)
            generated.append(output_path)

    generated_list = OUTPUT_DIR / '_generated_files.txt'
    generated_list.write_text(
        ''.join(f"{path.relative_to(ROOT)}\n" for path in generated),
        encoding='utf-8',
    )
    return generated


def main() -> None:
    generated = materialize()
    for path in generated:
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
