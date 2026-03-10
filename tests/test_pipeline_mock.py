from pathlib import Path

from crb.evaluation.runner import run_from_config


def test_mock_pipeline_creates_outputs(tmp_path: Path):
    result = run_from_config("configs/mock_mmlu_multiturn_oracle.yaml")
    assert result["metrics"]["accuracy"] >= 0.0
    assert result["num_items"] == 2
