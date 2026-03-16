import json
from pathlib import Path

from crb.config import load_run_config
from crb.evaluation.runner import execute_run
from crb.io.pools import export_single_turn_run_to_prediction_pool
from crb.io.results import read_jsonl


def test_single_turn_config_parses():
    config = load_run_config("configs/mock_mmlu_single_turn_pool.yaml")
    assert config.evaluation.evaluation_mode == "single_turn"
    assert config.evaluation.k == 0
    assert config.evaluation.manifest_k_values == [0]
    assert config.runtime.prediction_pool_root == "results/pools/mock_single_turn"


def test_single_turn_pipeline_exports_correct_and_incorrect_pools(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_single_turn_pool.yaml")
    config.runtime.output_root = str(tmp_path / "results")
    config.runtime.manifest_dir = str(tmp_path / "results" / "manifests")
    config.runtime.summary_csv = str(tmp_path / "results" / "summary" / "scoreboard.csv")
    config.runtime.log_dir = str(tmp_path / "logs")
    config.runtime.prediction_pool_root = str(tmp_path / "results" / "pools")
    config.runtime.skip_completed = False

    result = execute_run(config)

    dataset_pool_dir = tmp_path / "results" / "pools" / "mmlu_fixture" / "test"
    correct_records = read_jsonl(dataset_pool_dir / "correct.jsonl")
    incorrect_records = read_jsonl(dataset_pool_dir / "incorrect.jsonl")
    summary = json.loads((dataset_pool_dir / "summary.json").read_text(encoding="utf-8"))
    overall_summary = json.loads((tmp_path / "results" / "pools" / "latest_run_summary.json").read_text(encoding="utf-8"))

    assert result["evaluation_mode"] == "single_turn"
    assert summary["correct_items"] == 1
    assert summary["incorrect_items"] == 3
    assert summary["format_invalid_items"] == 0
    assert overall_summary["correct_items"] == 1
    assert overall_summary["incorrect_items"] == 3
    assert len(correct_records) == 1
    assert len(incorrect_records) == 3
    assert all(record["source_correct"] for record in correct_records)
    assert all(not record["source_correct"] for record in incorrect_records)
    assert all(record["answer_type"] == "mcq" for record in correct_records + incorrect_records)
    assert {record["answer"] for record in correct_records + incorrect_records} == {"A"}


def test_prediction_pool_export_drops_invalid_and_moves_items_between_buckets(tmp_path: Path):
    output_root = tmp_path / "pools"
    payload = {
        "run_id": "run-1",
        "timestamp": "2026-03-16T00:00:00Z",
        "model_name": "mock-model",
        "model_family": "mock",
        "thinking_mode": "off",
        "evaluation_mode": "single_turn",
        "per_item_results": [
            {
                "dataset_name": "toy",
                "split": "test",
                "item_id": "toy:test:1",
                "domain": "science",
                "subject": "physics",
                "question": "Q1",
                "choices": ["A", "B"],
                "answer_type": "mcq",
                "parsed_answer": "A",
                "normalized_gold_answer": "A",
                "correct": True,
                "parse_status": "parsed",
                "raw_output": "Answer: A",
                "parser_name": "mcq",
                "generation_controls": None,
            },
            {
                "dataset_name": "toy",
                "split": "test",
                "item_id": "toy:test:2",
                "domain": "science",
                "subject": "physics",
                "question": "Q2",
                "choices": ["A", "B"],
                "answer_type": "mcq",
                "parsed_answer": "A",
                "normalized_gold_answer": "B",
                "correct": False,
                "parse_status": "parsed",
                "raw_output": "Answer: A",
                "parser_name": "mcq",
                "generation_controls": None,
            },
            {
                "dataset_name": "toy",
                "split": "test",
                "item_id": "toy:test:3",
                "domain": "science",
                "subject": "physics",
                "question": "Q3",
                "choices": ["A", "B"],
                "answer_type": "mcq",
                "parsed_answer": None,
                "normalized_gold_answer": "A",
                "correct": False,
                "parse_status": "invalid",
                "raw_output": "garbage",
                "parser_name": "mcq",
                "generation_controls": None,
            },
        ],
    }
    export_single_turn_run_to_prediction_pool(
        payload=payload,
        output_root=output_root,
        source_result_json_path=tmp_path / "run-1.json",
    )

    dataset_pool_dir = output_root / "toy" / "test"
    assert [record["item_id"] for record in read_jsonl(dataset_pool_dir / "correct.jsonl")] == ["toy:test:1"]
    assert [record["item_id"] for record in read_jsonl(dataset_pool_dir / "incorrect.jsonl")] == ["toy:test:2"]

    payload["run_id"] = "run-2"
    payload["per_item_results"][1]["parsed_answer"] = "B"
    payload["per_item_results"][1]["correct"] = True
    export_single_turn_run_to_prediction_pool(
        payload=payload,
        output_root=output_root,
        source_result_json_path=tmp_path / "run-2.json",
    )

    correct_ids = [record["item_id"] for record in read_jsonl(dataset_pool_dir / "correct.jsonl")]
    incorrect_ids = [record["item_id"] for record in read_jsonl(dataset_pool_dir / "incorrect.jsonl")]
    assert correct_ids == ["toy:test:1", "toy:test:2"]
    assert incorrect_ids == []
