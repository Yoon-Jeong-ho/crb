from pathlib import Path
import json

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


def test_mock_pipeline_wrong_history_uses_deterministic_incorrect_dummy_answers(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_multiturn_wrong_history.yaml")
    config.runtime.output_root = str(tmp_path / "results")
    config.runtime.manifest_dir = str(tmp_path / "results" / "manifests")
    config.runtime.summary_csv = str(tmp_path / "results" / "summary" / "scoreboard.csv")
    config.runtime.log_dir = str(tmp_path / "logs")
    config.runtime.skip_completed = False
    result = execute_run(config)
    item = result["per_item_results"][0]
    gold_by_item_id = {}
    for record in (
        json.loads(line)
        for line in Path("data/fixtures/mmlu_fixture.jsonl").read_text(encoding="utf-8").splitlines()
    ):
        gold_by_item_id[record["item_id"]] = record["answer"]
        gold_by_item_id[f"mmlu_fixture:test:{record['item_id']}"] = record["answer"]
    assert item["history_construction_mode"] == "wrong_history"
    assert all(turn["answer_source"] == "wrong" for turn in item["dummy_turns"])
    assert all(turn["raw_output"] is None for turn in item["dummy_turns"])
    assert all(turn["normalized_answer"] != gold_by_item_id[turn["item_id"]] for turn in item["dummy_turns"])


def test_mock_pipeline_stored_history_uses_precomputed_pool_answers(tmp_path: Path):
    config = load_run_config("configs/mock_mmlu_multiturn_oracle.yaml")
    pool_path = tmp_path / "stored_pool.jsonl"
    pool_records = [
        {
            "item_id": "stored-1",
            "subject": "history",
            "domain": "humanities",
            "question": "Dummy question 1?",
            "choices": ["A1", "B1", "C1", "D1"],
            "answer": "B",
            "answer_type": "mcq",
            "source_raw_output": "Answer: B",
        },
        {
            "item_id": "stored-2",
            "subject": "history",
            "domain": "humanities",
            "question": "Dummy question 2?",
            "choices": ["A2", "B2", "C2", "D2"],
            "answer": "D",
            "answer_type": "mcq",
            "source_raw_output": "Answer: D",
        },
        {
            "item_id": "stored-3",
            "subject": "physics",
            "domain": "science",
            "question": "Dummy question 3?",
            "choices": ["A3", "B3", "C3", "D3"],
            "answer": "C",
            "answer_type": "mcq",
            "source_raw_output": "Answer: C",
        },
        {
            "item_id": "stored-4",
            "subject": "physics",
            "domain": "science",
            "question": "Dummy question 4?",
            "choices": ["A4", "B4", "C4", "D4"],
            "answer": "A",
            "answer_type": "mcq",
            "source_raw_output": "Answer: A",
        },
    ]
    pool_path.write_text(
        "\n".join(json.dumps(record) for record in pool_records) + "\n",
        encoding="utf-8",
    )

    config.runtime.output_root = str(tmp_path / "results")
    config.runtime.manifest_dir = str(tmp_path / "results" / "manifests")
    config.runtime.summary_csv = str(tmp_path / "results" / "summary" / "scoreboard.csv")
    config.runtime.log_dir = str(tmp_path / "logs")
    config.runtime.skip_completed = False
    config.evaluation.history_mode = "stored_history"
    config.evaluation.dummy_sources[0].local_path = str(pool_path)
    config.evaluation.dummy_sources[0].dataset_name = "stored_pool"
    config.evaluation.dummy_sources[0].split = "train"
    result = execute_run(config)

    item = result["per_item_results"][0]
    assert item["history_construction_mode"] == "stored_history"
    assert all(turn["answer_source"] == "stored" for turn in item["dummy_turns"])
    assert all(turn["parse_status"] == "stored" for turn in item["dummy_turns"])
    assert {turn["normalized_answer"] for turn in item["dummy_turns"]}.issubset({"A", "B", "C", "D"})
    assert any(turn["raw_output"] == "Answer: B" for turn in item["dummy_turns"])
