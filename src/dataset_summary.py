import pandas as pd
from pathlib import Path
import json

mut_data = pd.read_csv("data/processed/combined_mutations.csv")

mut_data_dedup = mut_data.drop_duplicates(subset = ["sample_id", "chromosome", "position", "ref", "alt"])

report = {}

# dataset statistics
report["data_info"] = {
			"num_records": int(len(mut_data_dedup) - 1),
			"num_samples": int(mut_data_dedup["sample_id"].nunique()),
			"num_genes": int(mut_data_dedup["gene"].nunique()),
			"mut_type":  int(mut_data_dedup["mutation_type"].nunique()),
			"mut_type_count": mut_data_dedup["mutation_type"].value_counts().to_dict()
}

# Mutation counts per cancer type
report["mut_per_cancer"] = (
				mut_data_dedup.groupby("cancer_type")
				.size()
				.to_dict()
)

# Top mutated genes
report["top_mutated_genes"] = (
				mut_data_dedup["gene"]
				.value_counts()
				.head(20)
				.to_dict()
)

# Top mutated genes and counts in each cancer type
report["top_mutated_genes_cancer"] = {}

for cancer, group in mut_data_dedup.groupby("cancer_type"):

    top_genes = (
        group["gene"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    report["top_mutated_genes_cancer"][cancer] = top_genes


output_file = "data/reports/dataset_summary.json"

with open(output_file, "w") as f:
	json.dump(
		report,
		f,
		indent = 4
)
print(f"datasummary saved to {output_file})")
