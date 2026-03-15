from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / 'configs/generated/qwen3_protocol_k_sweep_full'

JOBS = [
    {
        'slug': 'gpqa_off_canonical',
        'template': ROOT / 'configs/templates/qwen3_1p7b_gpqa_base.yaml',
        'thinking_mode': 'off',
        'evaluation_mode': 'multi_turn',
        'history_mode': 'oracle_history',
        'dummy_type': 'same_domain',
        'ks': [0, 4, 8],
    },
    {
        'slug': 'gsm8k_on_canonical',
        'template': ROOT / 'configs/templates/qwen3_1p7b_gsm8k_base.yaml',
        'thinking_mode': 'on',
        'evaluation_mode': 'single_turn_flattened',
        'history_mode': 'self_history',
        'dummy_type': 'cross_domain',
        'ks': [0, 4, 8],
    },
]


def apply_thinking_variant(config: dict, thinking_mode: str) -> None:
    if thinking_mode == 'off':
        config['model']['thinking_mode'] = 'off'
        config['model']['chat_template_kwargs']['enable_thinking'] = False
        config['decoding']['temperature'] = 0.7
        config['decoding']['top_p'] = 0.8
        config['decoding']['top_k'] = 20
        config['decoding']['max_tokens'] = 1024
    elif thinking_mode == 'on':
        config['model']['thinking_mode'] = 'on'
        config['model']['chat_template_kwargs']['enable_thinking'] = True
        config['decoding']['temperature'] = 0.6
        config['decoding']['top_p'] = 0.95
        config['decoding']['top_k'] = 20
        config['decoding']['max_tokens'] = 2048
    else:
        raise ValueError(f'Unsupported thinking_mode: {thinking_mode}')


def materialize() -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for job in JOBS:
        base = yaml.safe_load(job['template'].read_text(encoding='utf-8'))
        for k in job['ks']:
            config = deepcopy(base)
            config['experiment']['num_samples'] = None
            config['experiment']['name'] = (
                f"{config['experiment']['name']}_protocol_kfull_{job['slug']}_k{k}"
            )
            tags = list(config['experiment'].get('tags', []))
            tags.extend(['protocol_kfull', job['slug'], f'k{k}'])
            config['experiment']['tags'] = tags

            apply_thinking_variant(config, job['thinking_mode'])

            config['evaluation']['evaluation_mode'] = job['evaluation_mode']
            config['evaluation']['history_mode'] = job['history_mode']
            config['evaluation']['dummy_type'] = job['dummy_type']
            config['evaluation']['k'] = k

            out = OUTPUT_DIR / f"qwen3_{job['slug']}__k-{k}.yaml"
            out.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding='utf-8')
            created.append(out)

    (OUTPUT_DIR / '_generated_files.txt').write_text(
        ''.join(f"{p.relative_to(ROOT)}\n" for p in created),
        encoding='utf-8',
    )
    return created


def main() -> None:
    for path in materialize():
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
