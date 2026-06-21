# Phase 3: Statistical Analysis

import pandas as pd
from scipy.stats import chi2_contingency


df = pd.read_csv("data/processed/combined_mutations.csv")

tp53 = df[df["gene"] == "TP53"]

tp53["tp53_mut"] = True

table = pd.crosstab(
df["cancer_type"],
df["gene"] == "TP53"
)

chi2, p, dof, expected = \
	chi2_contingency(table)

print(p)

if p < 0.05:
	print(f"Rejecting  H0, accepting alternate i.e: TP53 mutation frequency differs accross different cancers since p val < 0.05 (p = {p:.4f}")
if p > 0.05:
	print(f"Accespting H0 i.e TP53 mutation frequency same accross different cancers.")


# Analysis 2
# Mutation Type vs Cancer

# Are SNV/INDEL frequencies different among cancers?

table = pd.crosstab(
	df['cancer_type'],
	df['mutation_type']
)

chi2_contingency(table)

print(table)
