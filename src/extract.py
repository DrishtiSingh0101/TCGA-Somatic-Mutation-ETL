# Extract TCGA Somatic Mutation Data free API

import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://api.gdc.cancer.gov/files"

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    "TCGA-BRCA",
    "TCGA-LUAD",
    "TCGA-COAD"
]

def get_maf_files(project_id):

    filters = {
        "op": "and",
        "content": [
            {
                "op": "=",
                "content": {
                    "field": "cases.project.project_id",
                    "value": project_id
                }
            },
            {
                "op": "=",
                "content": {
                    "field": "data_format",
                    "value": "MAF"
                }
            },
            {
                "op": "=",
                "content": {
                    "field": "access",
                    "value": "open"
                }
            }
        ]
    }

    params = {
        "filters": str(filters).replace("'", '"'),
        "format": "JSON",
        "size": 100
    }

    response = requests.get(
        BASE_URL,
        params=params
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    for project in PROJECTS:

        print(f"Searching {project}")

        data = get_maf_files(project)

        output_file = (
            OUTPUT_DIR /
            f"{project}_maf_metadata.json"
        )

        pd.json_normalize(
            data["data"]["hits"]
        ).to_json(
            output_file,
            orient="records",
            indent=2
        )

        print(
            f"Saved metadata -> {output_file}"
        )
