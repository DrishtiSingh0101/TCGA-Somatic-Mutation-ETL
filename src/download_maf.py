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

    cancer_type = meta_file.split("_")[0]

    print(cancer_type)

    df = pd.read_json(RAW_DIR / meta_file)

    df = df.head(50) 

    print(
        f"{meta_file}: {len(df)} files"
    )

    if len(df) == 0:
        continue

    for _, row in df.iterrows():

        file_id = row["id"]
        file_name = row["file_name"]

        new_file_name = f"{cancer_type}_{file_name}"
        output_path = DOWNLOAD_DIR / new_file_name

        # Skip already downloaded files
        if output_path.exists():
            print(f"Skipping existing file: {new_file_name}")
            continue

        print(f"Downloading {file_name}")

        response = requests.get(
            BASE_URL + file_id
        )

        if response.status_code != 200:

            print(
                f"Failed: {file_name}"
            )
            continue

        with open(output_path, "wb") as f:
            f.write(response.content)

#        print(f"Saved: {output_path}")
