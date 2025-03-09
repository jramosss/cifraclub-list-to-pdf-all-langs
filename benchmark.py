import matplotlib.pyplot as plt
import numpy as np

songs = [17, 275]
scraping_times = [492, 948]
pdf_times = [1155, 4608]

x = np.arange(len(songs))
bar_width = 20

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

scraping_axis = axs[0]
scraping_axis.bar(songs, scraping_times, color='orange', width=bar_width)
scraping_axis.set_xlabel('Number of Songs')
scraping_axis.set_ylabel('Time (ms)')
scraping_axis.set_title('Scraping Performance')
scraping_axis.set_xticks(songs)

# Mostrar valores encima de las barras
def add_labels(ax, data):
    for i, v in enumerate(data):
        ax.text(songs[i], v, f'{v}ms', ha='center', va='bottom')

add_labels(scraping_axis, scraping_times)

pdf_generation_axis = axs[1]
pdf_generation_axis.bar(songs, pdf_times, color='red', width=bar_width)
pdf_generation_axis.set_xlabel('Number of Songs')
pdf_generation_axis.set_ylabel('Time (ms)')
pdf_generation_axis.set_title('PDF Generation Performance')
pdf_generation_axis.set_xticks(songs)

add_labels(pdf_generation_axis, pdf_times)

plt.tight_layout()
plt.savefig('benchmark.png')
