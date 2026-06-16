import pandas as pd
from pathlib import Path
import glob

INPUT_DIR = Path("data/raw/maf_files")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(exist_ok=True)

all_dfs = []

for file in glob.glob(str(INPUT_DIR / "*.maf*")):

    print(f"Processing {file}")

    df = pd.read_csv(
        file,
        sep="\t",
        comment="#",
        low_memory=False
    )

    columns_to_keep = [
        "Hugo_Symbol",
        "Chromosome",
        "Start_Position",
        "Reference_Allele",
        "Tumor_Seq_Allele2",
        "Variant_Classification",
        "Tumor_Sample_Barcode"
    ]

    df = df[columns_to_keep]

    # Rename columns
    df.columns = [
        "gene",
        "chromosome",
        "position",
        "ref",
        "alt",
        "variant_classification",
        "sample_id"
    ]

    # Standardize gene names
    df["gene"] = df["gene"].str.upper()

    # Infer cancer type
    if "BRCA" in file:
        df["cancer_type"] = "BRCA"
    elif "LUAD" in file:
        df["cancer_type"] = "LUAD"
    elif "COAD" in file:
        df["cancer_type"] = "COAD"

    # Mutation type
    df["mutation_type"] = "SNV"

    mask = (
        df["ref"].str.len() !=
        df["alt"].str.len()
    )

    df.loc[mask, "mutation_type"] = "INDEL"

    all_dfs.append(df)

combined = pd.concat(all_dfs)

combined.to_csv(
    OUTPUT_DIR / "combined_mutations.csv",
    index=False
)

print(combined.shape)
print(combined.columns.tolist())
print(combined.head())
