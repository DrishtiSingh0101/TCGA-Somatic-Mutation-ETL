
# Does mutation burden differ between cancers?

# Compute burden

import pandas as pd
from scipy.stats import f_oneway

df = pd.read_csv(
    "data/processed/combined_mutations.csv"
)

burden = (
    df.groupby(
        ["sample_id",
         "cancer_type"]
    )
    .size()
    .reset_index(
        name="mutation_burden"
    )
)

groups = [
    g["mutation_burden"]
    for _, g in burden.groupby(
        "cancer_type"
    )
]

f,p = f_oneway(*groups)

print(f"F={f}")
print(f"p={p}")

if p < 0.05:
	print("Mutation burden differs across cancers.")
else:
	print("Mutation burden same across cancers.")
