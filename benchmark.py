import json
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Benchmark:
    language: str
    total_songs: int
    scrape_time: int
    pdf_generate_time: int

def plot_benchmark_comparison(benchmarks: List[Benchmark], filepath: str) -> None:
    languages = list(set(b.language for b in benchmarks))
    songs = sorted(set(b.total_songs for b in benchmarks))

    data_scraping = {lang: [] for lang in languages}
    data_pdf = {lang: [] for lang in languages}

    for song in songs:
        for lang in languages:
            benchmark = next((b for b in benchmarks if b.language == lang and b.total_songs == song), None)
            if benchmark:
                data_scraping[lang].append(benchmark.scrape_time)
                data_pdf[lang].append(benchmark.pdf_generate_time)
            else:
                data_scraping[lang].append(0)
                data_pdf[lang].append(0)

    x = np.arange(len(songs))
    bar_width = 0.2

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    scraping_axis = axs[0]

    for i, lang in enumerate(languages):
        scraping_axis.bar(x + i * bar_width, data_scraping[lang], bar_width, label=lang)
    scraping_axis.set_xlabel('Number of Songs')
    scraping_axis.set_ylabel('Time (ms)')
    scraping_axis.set_title('Scraping Performance Comparison')
    scraping_axis.set_xticks(x + bar_width * (len(languages) / 2 - 0.5))
    scraping_axis.set_xticklabels(songs)
    scraping_axis.legend()

    pdf_generation_axis = axs[1]
    for i, lang in enumerate(languages):
        pdf_generation_axis.bar(x + i * bar_width, data_pdf[lang], bar_width, label=lang)
    pdf_generation_axis.set_xlabel('Number of Songs')
    pdf_generation_axis.set_ylabel('Time (ms)')
    pdf_generation_axis.set_title('PDF Generation Performance Comparison')
    pdf_generation_axis.set_xticks(x + bar_width * (len(languages) / 2 - 0.5))
    pdf_generation_axis.set_xticklabels(songs)
    pdf_generation_axis.legend()

    plt.tight_layout()
    plt.savefig(filepath)

def get_benchmarks():
    folders = list(filter(lambda x: os.path.isdir(x), os.listdir('languages')))
    benchmarks: list[Benchmark] = []
    for language in ["typescript"]:
        process = subprocess.run(f"cd languages/{language} && bash run_benchmark.sh", capture_output=True, shell=True)
        out = process.stdout.decode('utf-8')
        parsed_output = json.loads(out)
        benchmark = Benchmark(language, parsed_output['total_songs'], parsed_output['scrape_time'], parsed_output['pdf_generate_time'])
        benchmarks.append(benchmark)
    return benchmarks


def group_benchmarks(benchmarks: list[Benchmark]):
    grouped_benchmarks = {}
    for benchmark in benchmarks:
        if benchmark.language not in grouped_benchmarks:
            grouped_benchmarks[benchmark.language] = []
        grouped_benchmarks[benchmark.language].append(benchmark)
    return grouped_benchmarks


if __name__ == '__main__':
    benchmarks = get_benchmarks()

    grouped_benchmarks = group_benchmarks(benchmarks)

    for language, benchmarks in grouped_benchmarks.items():
        plot_benchmark_comparison(benchmarks, f"benchmarks/{language}_benchmark.png")

