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
    benchmark_type: str  # "tiny" or "large"


def plot_benchmark_comparison(benchmarks: List[Benchmark], filepath: str, benchmark_type: str) -> None:
    # Filter benchmarks by type
    filtered_benchmarks = [b for b in benchmarks if b.benchmark_type == benchmark_type]
    
    if not filtered_benchmarks:
        print(f"No benchmarks found for type: {benchmark_type}")
        return
    
    languages = list(set(b.language for b in filtered_benchmarks))
    
    # For single benchmark type, we'll create a bar chart comparing languages
    scraping_times = []
    pdf_times = []
    lang_labels = []
    
    for lang in languages:
        benchmark = next((b for b in filtered_benchmarks if b.language == lang), None)
        if benchmark:
            scraping_times.append(benchmark.scrape_time)
            pdf_times.append(benchmark.pdf_generate_time)
            lang_labels.append(lang)
    
    # Sort languages by total time (scraping + pdf)
    total_times = [s + p for s, p in zip(scraping_times, pdf_times)]
    sorted_data = sorted(zip(lang_labels, scraping_times, pdf_times, total_times), key=lambda x: x[3])
    lang_labels, scraping_times, pdf_times, total_times = zip(*sorted_data)
    
    x = np.arange(len(lang_labels))
    bar_width = 0.35
    
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico de comparación de tiempos
    axs[0].bar(x - bar_width/2, scraping_times, bar_width, label='Scraping Time', alpha=0.8)
    axs[0].bar(x + bar_width/2, pdf_times, bar_width, label='PDF Generation Time', alpha=0.8)
    axs[0].set_xlabel("Programming Languages")
    axs[0].set_ylabel("Time (ms)")
    axs[0].set_title(f"Performance Comparison - {benchmark_type.title()} Benchmark\n({filtered_benchmarks[0].total_songs} songs)")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(lang_labels, rotation=45, ha='right')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)
    
    # Gráfico de tiempo total
    axs[1].bar(x, total_times, color='skyblue', alpha=0.8)
    axs[1].set_xlabel("Programming Languages")
    axs[1].set_ylabel("Total Time (ms)")
    axs[1].set_title(f"Total Time Comparison - {benchmark_type.title()} Benchmark\n({filtered_benchmarks[0].total_songs} songs)")
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(lang_labels, rotation=45, ha='right')
    axs[1].grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, (scrape, pdf, total) in enumerate(zip(scraping_times, pdf_times, total_times)):
        axs[0].text(i - bar_width/2, scrape + max(scraping_times) * 0.01, f'{scrape:.0f}', 
                   ha='center', va='bottom', fontsize=8)
        axs[0].text(i + bar_width/2, pdf + max(pdf_times) * 0.01, f'{pdf:.0f}', 
                   ha='center', va='bottom', fontsize=8)
        axs[1].text(i, total + max(total_times) * 0.01, f'{total:.0f}', 
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()


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
    
    benchmarks = []
    for benchmark_result in results:
        # Determine benchmark type based on total_songs or pdfFileName
        benchmark_type = "tiny"
        if "pdfFileName" in benchmark_result:
            if "large" in benchmark_result["pdfFileName"].lower():
                benchmark_type = "large"
        else:
            # Fallback: use total_songs to determine type
            if benchmark_result["total_songs"] > 100:  # Arbitrary threshold
                benchmark_type = "large"
        
        benchmarks.append(Benchmark(
            language,
            benchmark_result["total_songs"],
            benchmark_result["scrape_time"],
            benchmark_result["pdf_generate_time"],
            benchmark_type
        ))
    
    return benchmarks


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

    # Generate separate plots for tiny and large benchmarks
    plot_benchmark_comparison(benchmarks, "comparison_tiny.png", "tiny")
    plot_benchmark_comparison(benchmarks, "comparison_large.png", "large")
    
    print("Generated comparison plots:")
    print("- comparison_tiny.png: Comparison for tiny benchmarks")
    print("- comparison_large.png: Comparison for large benchmarks")
