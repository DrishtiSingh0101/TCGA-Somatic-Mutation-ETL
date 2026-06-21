import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# top_freq_genes dataframe
# columns:
# cancer_type, gene, mutation_frequency
top_freq_genes = pd.read_csv("data/processed/analysis/top_5_frequently_mutated_genes.csv")

cancer_order = ["LUAD", "COAD", "BRCA"]

# Colors
color_map = {
    "LUAD": "#66c2a5",
    "COAD": "#fc8d62",
    "BRCA": "#8da0cb"
}

# Sequential positions
x = np.arange(len(top_freq_genes))

fig, ax = plt.subplots(figsize=(14, 6))

bars = ax.bar(
    x,
    top_freq_genes["mutation_frequency"],
    color=[
        color_map[c]
        for c in top_freq_genes["cancer_type"]
    ]
)

# Gene labels
ax.set_xticks(x)
ax.set_xticklabels(
    top_freq_genes["gene"],
    rotation=0
)

# Frequency labels
for bar, value in zip(
    bars,
    top_freq_genes["mutation_frequency"]
):

    ax.text(
        bar.get_x() + bar.get_width()/2,
        value + 1,
        f"{value:.1f}%",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

# Cancer labels underneath groups
group_centers = []

for cancer in cancer_order:

    idx = top_freq_genes[
        top_freq_genes["cancer_type"] == cancer
    ].index

    center = idx.values.mean()

    group_centers.append(
        (center, cancer)
    )

for center, cancer in group_centers:

    ax.text(
        center,
        -7,
        cancer,
        ha="center",
        fontsize=14,
        fontweight="bold",
        color=color_map[cancer]
    )

ax.set_ylabel(
    "Mutation Frequency (%)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel(
    "Cancer Type / Gene Symbol",
    fontsize=14,
    fontweight="bold",
    labelpad=18
)

ax.set_title(
    "Top 5 Mutated Genes Grouped by Cancer Type",
    fontsize=18,
    fontweight="bold"
)

ax.set_ylim(
    0,
    max(top_freq_genes["mutation_frequency"]) + 10
)

plt.tight_layout()

plt.savefig(
    "data/plots/top5_mutated_genes_chatgpt.png",
    dpi=300,
    bbox_inches="tight"
)
