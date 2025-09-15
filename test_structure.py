import json
import os


def test_benchmark_exists():
    languages_dir = os.listdir("languages")
    for language in languages_dir:
        assert os.path.isdir(f"languages/{language}")
        assert os.path.exists(f"languages/{language}/benchmarks.json")


def test_benchmark_structure():
    languages_dir = os.listdir("languages")
    benchmarks = [f"languages/{language}/benchmarks.json" for language in languages_dir]
    for benchmark in benchmarks:
        j: list[dict[str, int]] = json.load(open(benchmark))
        print(benchmark)
        assert len(j) == 2
        assert "total_songs" in j[0]
        assert "scrape_time" in j[0]
        assert "pdf_generate_time" in j[0]


