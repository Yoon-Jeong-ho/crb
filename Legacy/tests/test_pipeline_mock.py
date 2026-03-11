from pathlib import Path

from crb.config import load_run_config
from crb.evaluation.runner import execute_run


def test_mock_pipeline_creates_outputs(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_multiturn_oracle.yaml")
    config.runtime.output_root = str(tmp_path / "results")
    config.runtime.manifest_dir = str(tmp_path / "results" / "manifests")
    config.runtime.summary_csv = str(tmp_path / "results" / "summary" / "scoreboard.csv")
    config.runtime.log_dir = str(tmp_path / "logs")
    config.runtime.skip_completed = False
    result = execute_run(config)
    assert result["metrics"]["accuracy"] >= 0.0
    assert result["num_items"] == 2


def test_mock_pipeline_records_generation_controls(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_multiturn_oracle_constrained_nothink.yaml")
    config.runtime.output_root = str(tmp_path / "results")
    config.runtime.manifest_dir = str(tmp_path / "results" / "manifests")
    config.runtime.summary_csv = str(tmp_path / "results" / "summary" / "scoreboard.csv")
    config.runtime.log_dir = str(tmp_path / "logs")
    config.runtime.skip_completed = False
    result = execute_run(config)
    item = result["per_item_results"][0]
    assert item["generation_controls"]["target_thinking_mode"] == "no_think"
    assert item["generation_controls"]["structured_choice"] == ["A", "B", "C", "D"]
    assert "/no_think" in item["prompt_preview"]
    assert "Answer: " in item["prompt_preview"]
