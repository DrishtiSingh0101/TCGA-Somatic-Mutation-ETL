import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Visualization 1: Sample Count per Cancer: Are the cohorts balanced?

sample_counts = pd.read_csv(
    "data/processed/analysis/sample_counts_per_cancer_type.csv"
)

plt.figure(figsize=(6,4))

plt.bar(
    sample_counts["cancer_type"],
    sample_counts["sample_count"]
)

plt.title("Number of Samples per Cancer Type")
plt.xlabel("Cancer Type")
plt.ylabel("Number of Samples")

plt.tight_layout()

plt.savefig(
    "data/plots/sample_counts.png",
    dpi=300
)

# Visualization 2: Mutation Counts per Cancer
# Which cohort contributes the largest number of mutation records?

mutation_counts = pd.read_csv(
    "data/processed/analysis/mut_count_in_cancer_type.csv"
)

plt.figure(figsize=(6,4))

plt.bar(
    mutation_counts["cancer_type"],
    mutation_counts["mut_counts"]
)

plt.title("Mutation Records per Cancer Type")
plt.xlabel("Cancer Type")
plt.ylabel("Mutation Counts")

plt.tight_layout()

plt.savefig(
    "data/plots/mut_per_cancer.png",
    dpi=300
)


# Visualization 3: Mutation Burden Distribution

df = pd.read_csv(
    "data/processed/analysis/mutation_burden.csv"
)

#burden = (
#    df.groupby(
#        ["sample_id","cancer_type"]
#    )
#    .size()
#    .reset_index(
#        name="mutation_burden"
#    )
#)

plt.figure(figsize=(8,5))

df.boxplot(
    column="mutation_burden",
    by="cancer_type"
)

plt.title(
    "Mutation Burden by Cancer Type"
)

plt.suptitle("")

plt.xlabel("Cancer Type")
plt.ylabel("Mutations per Sample")

plt.tight_layout()

plt.savefig(
    "data/plots/mutation_burden_boxplot.png",
    dpi=300
)

# Visualization 4: Top Mutated Genes Overall


df = pd.read_csv("data/processed/combined_mutations.csv")
top_genes = (df["gene"]
    .value_counts()
    .reset_index(name = "mut_count")
    .rename(columns = {"index": "gene"})
)
top_10 = top_genes.head(10)

plt.figure(figsize= (8,5))

plt.barh(
    top_10["gene"],
    top_10["mut_count"]
)

plt.xlabel("mutattion counts")
plt.ylabel("gene")

plt.title("Top 10 most mutated genes acrross all cancers")

plt.tight_layout()

plt.savefig(
    "data/plots/top_10_mut_genes.png",
    dpi=300
)

# Visualization 5: Top Genes per Cancer

freq_genes_cancer = pd.read_csv("data/processed/analysis/top_5_frequently_mutated_genes.csv")

# 1. Filter down to the top 5 genes per cancer type
#top5_df = (
#    freq_genes_cancer.sort_values(["cancer_type", "mutation_frequency"], ascending=[True, False])
#    .groupby("cancer_type")
#    .head(5)
#)

# 2. Set the overall visual style
sns.set_theme(style="whitegrid")

# 3. Create a FacetGrid (one subplot row/column per cancer type)
# 'sharey=False' is critical so each cancer shows its own top 5 genes!
g = sns.FacetGrid(
    freq_genes_cancer,
    col="cancer_type",
    col_wrap=3,
    sharey=False,
    height=4,
    aspect=1.2,
)

# 4. Map a horizontal barplot onto the grid
g.map_dataframe(
    sns.barplot,
    x="mutation_frequency",
    y="gene",
    hue="cancer_type",  # Colors each cancer differently
    palette="viridis",  # Clean color scheme
    legend=False,
)

# 5. Clean up axis labels and titles
g.set_axis_labels("Mutation Frequency (%)", "Gene")
g.set_titles(col_template="{col_name}")  # Titles will just be 'BRCA', 'LUAD', etc.

# Tight layout stops labels from clipping at the edges
plt.tight_layout()

# 6. Save and Display
plt.savefig("data/plots/top_5_freq_mut_genes_separately.png", dpi=300, bbox_inches="tight")


# 1. Filter down to the top 5 genes per cancer type

# 2. Create a combined multi-line label: Cancer Type on top, Gene Symbol underneath
freq_genes_cancer["x_label"] = freq_genes_cancer["cancer_type"] + "\n" + freq_genes_cancer["gene"]

# 3. Set a wider figure layout so the bars have plenty of breathing room
plt.figure(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# 4. Plot using the new combined label. 
# We use 'hue="cancer_type"' to give each cancer group a distinct, solid color block.
ax = sns.barplot(
    data=freq_genes_cancer,
    x="x_label",
    y="mutation_frequency",
    hue="cancer_type",
    dodge=False,  # Stops Seaborn from trying to space out the hues
    palette="Set2",  # Clean, publication-ready color palette
)

# 5. Add data labels perfectly centered on top of the widened bars
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", padding=4, fontsize=10, weight="bold")

# 6. Fine-tune aesthetics and clear messy overlaps
plt.title(
    "Top 5 Mutated Genes Across Cancer Types",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Cancer Type / Gene Symbol", fontsize=12, labelpad=10)
plt.ylabel("Mutation Frequency (%)", fontsize=12)

# Clean up the legend since the X-axis labels already explicitly name the cancers
plt.legend().remove()

# Increase spacing below the plot so long labels don't get clipped
plt.tight_layout()

# 7. Save and show
plt.savefig("data/plots/widened_nested_top5_mut_freq_plot.png", dpi=300, bbox_inches="tight")


# 2. Set up a wide figure layout
fig, ax = plt.subplots(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# 3. Define unique sequential positions for all 15 bars (0 to 14)
# This prevents different cancers with the same gene (e.g. TP53) from overlapping
x_positions = np.arange(len(freq_genes_cancer))
palette_name = "Set2"
colors = sns.color_palette(palette_name)

# 4. Plot using explicit numerical X positions
sns.barplot(
    data=freq_genes_cancer,
    x=x_positions,
    y="mutation_frequency",
    hue="cancer_type",
    dodge=False,  # Keeps bars adjacent without leaving blank placeholders
    palette=palette_name,
    ax=ax,
)

# 5. Set the individual gene names directly under each bar
ax.set_xticks(x_positions)
ax.set_xticklabels(freq_genes_cancer["gene"], fontsize=8)

# 6. Add the centered, color-matched cancer labels UNDER the genes
# We use a blended transform: X uses data positions (0-14), Y uses plot coordinates (0=bottom, 1=top)
unique_cancers = freq_genes_cancer["cancer_type"].unique()

for i, cancer in enumerate(unique_cancers):
    # Find all the bar indices belonging to this specific cancer type
    cancer_indices = np.where(freq_genes_cancer["cancer_type"] == cancer)[0]
    center_x = cancer_indices.mean()  # Automatically finds the true center bar

    # Add the single cancer label further down
    ax.text(
        x=center_x,
        y=-0.08,  # Places text ~15% below the bottom axis line
        s=cancer,
        transform=ax.get_xaxis_transform(),  # Magic transform for flawless alignment
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
        color=colors[i],  # Matches the color of the text to its corresponding bars!
    )

# 7. Add data labels on top of each bar
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", padding=4, fontsize=10, weight="bold")

# 8. Clean up styling
plt.title(
    "Top 5 Mutated Genes Grouped by Cancer Type",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
#plt.xlabel("", labelpad=25)  # Leave room for our custom bottom labels
plt.xlabel("Cancer Type / Gene Symbol", fontsize=10, labelpad=18, weight="bold")
plt.ylabel("Mutation Frequency (%)", fontsize=12, weight="bold")

# Remove the default legend since our color-matched text explains it perfectly
ax.get_legend().remove()

# Make sure the bottom labels aren't cut off when saving
plt.subplots_adjust(bottom=0.2)

# 9. Save and show
plt.savefig("data/plots/top5_freq_mut_ganes_per_cancer.png", dpi=300, bbox_inches="tight")


# Visualization 6: Gene Frequency Heatmap

df = pd.read_csv("data/processed/analysis/gene_mutation_frequency.csv")
heatmap_df = (
    df
    .pivot(
        index="gene",
        columns="cancer_type",
        values="mutation_frequency"
    )
)

plt.figure(figsize=(8,6))

sns.heatmap(
    heatmap_df,
    annot=True
)

plt.title(
    "Mutation Frequency Heatmap"
)

plt.savefig("data/plots/mut_freq_heatmap.png", dpi=300, bbox_inches="tight")
