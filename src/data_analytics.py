from sqlalchemy import create_engine
import pandas as pd

# Question 1: How many mutations are present in each cancer?

query = """
SELECT cancer_type, 
	COUNT(*) AS MUT_COUNTS
FROM mutations
GROUP BY cancer_type
ORDER BY mut_counts DESC;
"""

engine = create_engine(
	"postgresql://drishti:postgresql1stpw@localhost:5432/cancerdb"
)

df = pd.read_sql(
	query, engine
)

df.to_csv("data/processed/analysis/mut_count_in_cancer_type.csv", index = False)


# Question 2: What are the most frequently mutated genes?

query = """
SELECT GENE,
	COUNT(*) AS G_MUT_COUNT
FROM MUTATIONS
GROUP BY GENE
ORDER BY G_MUT_COUNT DESC;
"""

df = pd.read_sql(
	query, engine)

df.to_csv("data/processed/analysis/top_mutated_genes.csv", index = False)

# Question 3: What proportion of mutations are SNVs vs INDELs?

query = """
SELECT MUTATION_TYPE, 
	COUNT(*) AS MUT_COUNT
FROM MUTATIONS
GROUP BY MUTATION_TYPE
ORDER BY MUT_COUNT DESC;
"""


df = pd.read_sql(
        query, engine)

df.to_csv("data/processed/analysis/mutation_type_count.csv", index = False)

query = """
SELECT CANCER_TYPE,MUTATION_TYPE,
	COUNT(MUTATION_TYPE) AS MUT_COUNT
FROM MUTATIONS
GROUP BY CANCER_TYPE, MUTATION_TYPE
ORDER BY MUT_COUNT DESC;
"""


df = pd.read_sql(
        query, engine)

df.to_csv("data/processed/analysis/mutation_type_per_cancer.csv", index = False)

# Question 4: Which mutation classifications are most common?

query = """
SELECT variant_classification,
       COUNT(*) AS count
FROM mutations
GROUP BY variant_classification
ORDER BY count DESC;
"""

df = pd.read_sql(
        query, engine)

df.to_csv("data/processed/analysis/var_class_count.csv", index = False)

# Real Biological questions:

# Sample level analysis:

# Number of samples in each cancer to see if the dataset is balanced:

mut_data = pd.read_csv("data/processed/combined_mutations.csv")
#sample_count = (
#	mut_data.groupby("cancer_type")["sample_id"].nunique()
#)

#print(sample_count.head(5))

query ="""
SELECT CANCER_TYPE,
	COUNT(DISTINCT SAMPLE_ID) AS SAMPLE_COUNT
FROM MUTATIONS
GROUP BY CANCER_TYPE
ORDER BY SAMPLE_COUNT DESC;
"""

df = pd.read_sql(
	query, engine
)

df.to_csv("data/processed/analysis/sample_counts_per_cancer_type.csv", index = False)

# How many mutation events are observed in each cancer?

# Done already

# Do patients in COAD carry more mutations than patients in BRCA? : Mutation burden


burden = (
    mut_data.groupby(["sample_id","cancer_type"])
      .size()
      .reset_index(name="mutation_burden")
)

#mean_mut_burder = burden.groupby("cancer_type")[["mutation_burden"]].mean()

#mean_mut_burder.to_csv(
#    "data/processed/analysis/mean_mutation_burden.csv"
#)

burden.to_csv(
    "data/processed/analysis/mutation_burden.csv",
    index=False
)

burden_summary = (
    burden.groupby(
        "cancer_type"
    )["mutation_burden"]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max",
        "std"
    ])
)

print(burden_summary)

burden_summary.to_csv(
    "data/processed/analysis/mutation_burden_summary.csv"
)

# Which genes are commonly altered in cancer? Frequently mutated genes in BRCA/COAD/LUAD?
#OR
# What defines the mutational landscape of each cancer?

gene_counts = (
    mut_data.groupby(["cancer_type", "gene"]).size().reset_index(name="count")
)

# 2. Get the top 3 most frequent genes for each cancer type
top_genes_per_cancer = (
    gene_counts.groupby("cancer_type")
    .apply(lambda x: x.nlargest(5, "count"), include_groups=False)
    .reset_index()
)

top_genes_per_cancer.to_csv("data/processed/analysis/top_10_mutated_genes_in_cancer.csv")

# What percentage of patients carry mutations in a gene? eg. TP53 mutated in 25/50 BRCA samples (50%)

# 1. Get total unique samples per cancer type as a mapping dictionary(series to use .map)
total_samples = mut_data.groupby("cancer_type")["sample_id"].nunique()

# 2. Count mutated samples for every cancer/gene combination at once

freq_df = (
    mut_data.groupby(["cancer_type", "gene"])["sample_id"]
    .nunique()
    .reset_index(name="mutated_samples")
)

#print(freq_df.head())

# 3. Add total_samples using map, and calculate percentage

freq_df["total_samples"] = freq_df["cancer_type"].map(total_samples)
freq_df["mutation_frequency"] = (
    freq_df["mutated_samples"] / freq_df["total_samples"] * 100
)

# 4. Sort and save

freq_df = freq_df.sort_values(
    ["cancer_type", "mutation_frequency"], ascending=[False, False]
)
freq_df.to_csv("data/processed/analysis/gene_mutation_frequency.csv", index=False)

# ⭐ 5. EXTRACT ONLY THE TOP 5 GENES PER CANCER TYPE ⭐
top5_df = freq_df.groupby("cancer_type").head(5)

#print(top5_df)

top5_df.to_csv("data/processed/analysis/top_5_frequently_mutated_genes.csv")
