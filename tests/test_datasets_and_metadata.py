from crb.config import load_run_config
from crb.io.results import SCOREBOARD_COLUMNS


def test_thinking_metadata_parses_from_config():
    config = load_run_config('configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_on.yaml')
    assert config.model.model_family == 'qwen3'
    assert config.model.thinking_mode == 'on'
    assert config.model.chat_template_kwargs['enable_thinking'] is True


def test_scoreboard_columns_include_reasoning_fields():
    assert 'model_family' in SCOREBOARD_COLUMNS
    assert 'thinking_mode' in SCOREBOARD_COLUMNS


def test_aime_fixture_config_like_numeric_metadata():
    config = load_run_config('configs/qwen3_1p7b_aime_multiturn_oracle_same_k2_thinking_off.yaml')
    assert config.evaluation.target.adapter == 'aime'
    assert config.evaluation.target.dataset_name == 'aime'


def test_gpqa_config_uses_gpqa_adapter():
    config = load_run_config('configs/qwen3_1p7b_gpqa_multiturn_oracle_same_k2_thinking_off.yaml')
    assert config.evaluation.target.adapter == 'gpqa'
    assert config.evaluation.target.dataset_name == 'gpqa'
