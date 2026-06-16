import pandas as pd

df = pd.read_json(
    "data/raw/TCGA-BRCA_maf_metadata.json"
)

print(df.columns)
print(df.head())
print(df[['id', 'file_name']].head())
