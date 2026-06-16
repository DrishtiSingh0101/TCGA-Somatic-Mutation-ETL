import pandas as pd

mut_data = pd.read_csv("data/processed/combined_mutations.csv")

report = {}

# Missing gene or positions

report["missing_genes"] = mut_data["gene"].isna().sum()

report["Missing_pos"] = mut_data["position"].isna().sum()

# Duplicated variants

report["duplicates"] = mut_data.duplicated(
				subset = [
					"sample_id",
					"chromosome",
					"position",
					"ref",
					"alt"
				]).sum()



# Check if there are any invalid chromosome

valid_chr = [str(i) for i in range(1,23)] + ["X", "Y", "MT", "M"] + [f"chr{i}" for i in range(1,23)] + ["chrX", "chrY", "chrMT", "chrM"]

report["invalid_chr"] = (~mut_data["chromosome"]
				.astype(str)
				.isin(valid_chr)).sum()


quality_df = pd.DataFrame(
		report.items(),
		columns = ["check", "count"]
)

quality_df.to_csv("data/reports/quality_report.csv", index = False)

print(quality_df)
