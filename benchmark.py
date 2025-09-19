import argparse
import concurrent.futures
import json
import os
import subprocess
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Benchmark:
    language: str
    total_songs: int
    scrape_time: int
    pdf_generate_time: int


def plot_benchmark_comparison(benchmarks: List[Benchmark], filepath: str) -> None:
    languages = list(set(b.language for b in benchmarks))
    songs = sorted(set(b.total_songs for b in benchmarks))

    # Organizar datos
    data_scraping = {lang: [] for lang in languages}
    data_pdf = {lang: [] for lang in languages}

    for song in songs:
        for lang in languages:
            benchmark = next(
                (b for b in benchmarks if b.language == lang and b.total_songs == song),
                None,
            )
            data_scraping[lang].append(benchmark.scrape_time if benchmark else 0)
            data_pdf[lang].append(benchmark.pdf_generate_time if benchmark else 0)

    # Ordenar lenguajes por rendimiento promedio (menor tiempo = mejor rendimiento)
    avg_scraping_times = {lang: np.mean(data_scraping[lang]) for lang in languages}
    avg_pdf_times = {lang: np.mean(data_pdf[lang]) for lang in languages}

    languages_sorted_scraping = sorted(languages, key=lambda lang: avg_scraping_times[lang])
    languages_sorted_pdf = sorted(languages, key=lambda lang: avg_pdf_times[lang])

    x = np.arange(len(songs))
    bar_width = 0.1

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico de scraping ordenado por rendimiento
    for i, lang in enumerate(languages_sorted_scraping):
        axs[0].bar(x + i * bar_width, data_scraping[lang], bar_width, label=lang)
    axs[0].set_xlabel("Number of Songs")
    axs[0].set_ylabel("Time (ms)")
    axs[0].set_title("Scraping Performance Comparison (Sorted by Performance)")
    axs[0].set_xticks(x + bar_width * (len(languages_sorted_scraping) / 2 - 0.5))
    axs[0].set_xticklabels(songs)
    axs[0].legend()

    # Gráfico de PDF ordenado por rendimiento
    for i, lang in enumerate(languages_sorted_pdf):
        axs[1].bar(x + i * bar_width, data_pdf[lang], bar_width, label=lang)
    axs[1].set_xlabel("Number of Songs")
    axs[1].set_ylabel("Time (ms)")
    axs[1].set_title("PDF Generation Performance Comparison (Sorted by Performance)")
    axs[1].set_xticks(x + bar_width * (len(languages_sorted_pdf) / 2 - 0.5))
    axs[1].set_xticklabels(songs)
    axs[1].legend()

    plt.tight_layout()
    plt.savefig(filepath)


def run_benchmark(language: str, generate: bool, local: bool = False, verbose: bool = False) -> List[Benchmark]:
    if generate:
        print(f"Running benchmarks for {language}")
        local_flag = " --local" if local else ""
        subprocess.run(
            f"cd languages/{language} && chmod +x run_benchmark.sh && bash run_benchmark.sh{local_flag}",
            shell=True,
            stdout=subprocess.DEVNULL if not verbose else None,
            stderr=subprocess.DEVNULL if not verbose else None,
        )
    results = json.load(open(f"languages/{language}/benchmarks.json"))
    return [
        Benchmark(
            language,
            benchmark_result["total_songs"],
            benchmark_result["scrape_time"],
            benchmark_result["pdf_generate_time"],
        )
        for benchmark_result in results
    ]


def get_benchmarks(*, generate: bool = True, local: bool = False, verbose: bool = False):
    folders = list(
        filter(lambda x: os.path.isdir(f"languages/{x}"), os.listdir("languages"))
    )
    benchmarks: list[Benchmark] = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(run_benchmark, language, generate, local, verbose) for language in folders
        ]
        for future in concurrent.futures.as_completed(futures):
            benchmarks.extend(future.result())

    return benchmarks


if __name__ == "__main__":
    # add CLI options to --plot-only and --local
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--plot-only", action="store_true", help="Plot the benchmark results only"
    )
    parser.add_argument(
        "--local", action="store_true", help="Run benchmarks locally instead of using Docker"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Run benchmarks with verbose output"
    )

    args = parser.parse_args()

    benchmarks = get_benchmarks(generate=(not args.plot_only), local=args.local, verbose=args.verbose)

    plot_benchmark_comparison(benchmarks, "comparision.png")
