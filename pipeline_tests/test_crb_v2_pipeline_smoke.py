from pathlib import Path

from crb_v2.pipeline import run_pipeline


def test_mock_pipeline_runs_end_to_end_and_builds_prefix_consistent_manifests(tmp_path):
    config_path = Path("configs_v2/pilot/mock_fixture_smoke.yaml")
    result = run_pipeline(config_path)
    root = Path(result["experiment_root"])
    assert root.exists()

    summary_rows = root / "aggregate" / "summary_rows.csv"
    assert summary_rows.exists()

    manifest_k4 = root / "pools" / "mock_model" / "fixture_mcq" / "same_benchmark" / "model_correct.json"
    payload = __import__("json").loads(manifest_k4.read_text(encoding="utf-8"))
    for entry in payload["entries"]:
        ordered_ids = entry["ordered_dummy_ids"]
        assert ordered_ids[:2] == ordered_ids[:4][:2]

    incorrect_pool = root / "baseline" / "mock_model" / "fixture_mcq" / "incorrect_pool.jsonl"
    rows = [__import__("json").loads(line) for line in incorrect_pool.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows
    assert all(row["provenance"] == "model_incorrect" for row in rows)

    numeric_summary = __import__("json").loads((root / "baseline" / "mock_model" / "fixture_numeric" / "summary.json").read_text(encoding="utf-8"))
    assert numeric_summary["format_failure_count"] == 0
    assert numeric_summary["correct_count"] > 0
    assert numeric_summary["incorrect_count"] > 0
