import pandas as pd
import requests
from pathlib import Path

RAW_DIR = Path("data/raw")
DOWNLOAD_DIR = RAW_DIR / "maf_files"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

metadata_files = [
    "TCGA-BRCA_maf_metadata.json",
    "TCGA-COAD_maf_metadata.json",
    "TCGA-LUAD_maf_metadata.json"
]

BASE_URL = "https://api.gdc.cancer.gov/data/"


for meta_file in metadata_files:

    df = pd.read_json(RAW_DIR / meta_file)

    if len(df) == 0:
        continue

    # Download first file only
    row = df.iloc[0]

    file_id = row["id"]
    file_name = row["file_name"]

    print(f"Downloading {file_name}")

    response = requests.get(BASE_URL + file_id)

    output_path = DOWNLOAD_DIR / file_name

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Saved: {output_path}")
