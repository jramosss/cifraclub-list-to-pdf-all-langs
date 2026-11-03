import json
from pathlib import Path

from benchmark import run_benchmark


def test_run_benchmark_keeps_csharp_large_result(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    csharp_dir = Path("languages/csharp")
    csharp_dir.mkdir(parents=True)
    json.dump(
        [
            {"total_songs": 24, "scrape_time": 700, "pdf_generate_time": 800},
            {"total_songs": 327, "scrape_time": 135, "pdf_generate_time": 747},
        ],
        open(csharp_dir / "benchmarks.json", "w"),
    )

    benchmarks = run_benchmark("csharp", generate=False)

    assert len(benchmarks) == 2
    assert benchmarks[1].benchmark_type == "large"
    assert benchmarks[1].total_songs == 327


def test_run_benchmark_keeps_non_csharp_large_result(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    python_dir = Path("languages/python")
    python_dir.mkdir(parents=True)
    json.dump(
        [
            {"total_songs": 24, "scrape_time": 300, "pdf_generate_time": 400},
            {"total_songs": 327, "scrape_time": 135, "pdf_generate_time": 747},
        ],
        open(python_dir / "benchmarks.json", "w"),
    )

    benchmarks = run_benchmark("python", generate=False)

    assert len(benchmarks) == 2
    assert benchmarks[1].benchmark_type == "large"
