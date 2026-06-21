import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv(
    "data/processed/combined_mutations.csv"
)

# Step 1: Create a sample-level table.

samples = (
    df[["sample_id",
        "cancer_type"]]
    .drop_duplicates()
)

tp53_samples = (
    df[df["gene"] == "TP53"]
    ["sample_id"]
    .unique()
)

samples["TP53_mut"] = (
    samples["sample_id"]
    .isin(tp53_samples)
)

# Step 2: Create contingency table

table = pd.crosstab(
    samples["cancer_type"],
    samples["TP53_mut"]
)

print(table)

# Step 3: Run Chi-square

chi2, p, dof, expected = (
    chi2_contingency(table)
)

print(f"Chi2={chi2}")
print(f"p-value={p}")

if p < 0.05:
	print("TP53 mutation frequency differs significantly among cancers")
else:
	print("TP53 mutation frequency is not changing significantly among cancers")
