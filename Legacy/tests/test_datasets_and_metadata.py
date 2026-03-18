from crb.config import load_run_config
from crb.datasets import load_items
from crb.schemas import DataSourceConfig
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


def test_generation_control_config_parses():
    config = load_run_config('configs/mock_mmlu_multiturn_oracle_constrained_nothink.yaml')
    assert config.decoding.target_choice_from_item_choices is True
    assert config.prompt.target_thinking_mode == 'no_think'
    assert config.prompt.target_response_prefill == 'Answer: '


def test_wrong_history_config_parses():
    config = load_run_config('configs/mock_mmlu_multiturn_wrong_history.yaml')
    assert config.evaluation.history_mode == 'wrong_history'


def test_single_turn_pool_loader_resolves_pool_path(tmp_path):
    pool_root = tmp_path / "results" / "pools" / "single_turn"
    pool_file = pool_root / "qwen3_1p7b" / "thinking_off" / "gpqa" / "train" / "correct.jsonl"
    pool_file.parent.mkdir(parents=True, exist_ok=True)
    pool_file.write_text(
        '{"dataset_name":"gpqa","split":"train","item_id":"gpqa:train:demo","domain":"science","subject":"biology","question":"Demo?","choices":["A","B","C","D"],"answer":"A","answer_type":"mcq","source_correct":true}\n',
        encoding="utf-8",
    )
    items = load_items(
        DataSourceConfig(
            dataset_name="gpqa",
            adapter="single_turn_pool",
            split="train",
            pool_root=str(pool_root),
            pool_model_slug="qwen3_1p7b",
            pool_thinking_mode="off",
            pool_label="correct",
        )
    )
    assert len(items) == 1
    assert items[0].item_id == "gpqa:train:demo"
    assert items[0].answer == "A"


def test_single_turn_pool_loader_accepts_boolean_thinking_mode(tmp_path):
    pool_root = tmp_path / "results" / "pools" / "single_turn"
    pool_file = pool_root / "qwen3_1p7b" / "thinking_off" / "gsm8k" / "test" / "incorrect.jsonl"
    pool_file.parent.mkdir(parents=True, exist_ok=True)
    pool_file.write_text(
        '{"dataset_name":"gsm8k","split":"test","item_id":"gsm8k:test:1","domain":"math","subject":"arithmetic","question":"Q?","answer":"3","answer_type":"numeric"}\n',
        encoding="utf-8",
    )
    items = load_items(
        DataSourceConfig(
            dataset_name="gsm8k",
            adapter="single_turn_pool",
            split="test",
            pool_root=str(pool_root),
            pool_model_slug="qwen3_1p7b",
            pool_thinking_mode=False,
            pool_label="incorrect",
        )
    )
    assert len(items) == 1
    assert items[0].item_id == "gsm8k:test:1"


def test_single_turn_pool_loader_falls_back_to_legacy_boolean_pool_dir(tmp_path):
    pool_root = tmp_path / "results" / "pools" / "single_turn"
    pool_file = pool_root / "qwen25_1p5b" / "thinking_False" / "gpqa" / "train" / "correct.jsonl"
    pool_file.parent.mkdir(parents=True, exist_ok=True)
    pool_file.write_text(
        '{"dataset_name":"gpqa","split":"train","item_id":"gpqa:train:legacy","domain":"science","subject":"biology","question":"Legacy?","choices":["A","B","C","D"],"answer":"B","answer_type":"mcq"}\n',
        encoding="utf-8",
    )
    items = load_items(
        DataSourceConfig(
            dataset_name="gpqa",
            adapter="single_turn_pool",
            split="train",
            pool_root=str(pool_root),
            pool_model_slug="qwen25_1p5b",
            pool_thinking_mode="off",
            pool_label="correct",
        )
    )
    assert len(items) == 1
    assert items[0].item_id == "gpqa:train:legacy"
    assert items[0].answer == "B"
