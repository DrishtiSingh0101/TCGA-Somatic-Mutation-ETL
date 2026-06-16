# create_project_structure.py

from pathlib import Path

folders = [
    "data/raw",
    "data/processed",
    "data/reports",
    "src",
    "notebooks",
    "sql",
    "dashboard"
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

files = [
    "src/extract.py",
    "src/transform.py",
    "src/quality_check.py",
    "src/load.py",
    "src/analysis.py",
    "requirements.txt",
    "README.md",
    ".gitignore"
]

for file in files:
    Path(file).touch(exist_ok=True)

print("Project structure created successfully!")
