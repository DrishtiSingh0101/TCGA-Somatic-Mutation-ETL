# Cancer Mutation Intelligence Platform - TCGA-Somatic-Mutation-ETL

An end-to-end ETL and analytics pipeline for extracting, transforming, validating, and analyzing somatic mutation data from The Cancer Genome Atlas (TCGA) across multiple cancer types.

---

## Project Overview

Cancer genomics studies generate large-scale somatic mutation datasets that require robust pipelines for extraction, preprocessing, quality assessment, and downstream analysis. This project aims to build a reproducible ETL (Extract-Transform-Load) workflow for processing TCGA mutation data and generating analytics-ready datasets.

The project was developed as a hands-on exercise to learn Data Engineering, SQL, statistical analysis, and data science workflows while leveraging prior experience in bioinformatics and cancer genomics.

---

## Objectives

* Extract somatic mutation data from TCGA using the GDC API.
* Transform raw mutation files into standardized analytics-ready datasets.
* Perform automated data quality checks and profiling.
* Generate summary statistics and mutation reports.
* Load processed data into a SQL database for querying and analysis.
* Perform statistical analyses to identify mutation patterns across cancer types.
* Build visualizations and dashboards for genomic insights.

---

## Dataset

### Source

* The Cancer Genome Atlas (TCGA)
* Genomic Data Commons (GDC) API

### Cancer Types Included

* BRCA: Breast Invasive Carcinoma
* LUAD: Lung Adenocarcinoma
* COAD: Colon Adenocarcinoma

### Data Type

* Somatic Mutation Annotation Format (MAF)

---

## ETL Workflow

```text
Extract Metadata (GDC API)
            ↓
Download MAF Files
            ↓
Transform Raw Data
            ↓
Data Quality Checks
            ↓
Generate Summary Reports
            ↓
Load into PostgreSQL
            ↓
SQL Analytics
            ↓
Statistical Analysis
            ↓
Visualization Dashboard
```

---

## Project Structure

```text
Cancer-Mutation-Intelligence-Platform/
│
├── data/
│   ├── raw/
│   │   ├── TCGA-BRCA_maf_metadata.json
│   │   ├── TCGA-LUAD_maf_metadata.json
│   │   ├── TCGA-COAD_maf_metadata.json
│   │   └── maf_files/
│   │
│   ├── processed/
│   │   └── combined_mutations.csv
│   │
│   └── reports/
│       ├── quality_report.csv
│       └── dataset_summary.json
│
├── src/
│   ├── extract.py
│   ├── download_maf.py
│   ├── transform.py
│   ├── quality_check.py
│   └── dataset_summary.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Steps Completed

### Step 1: Project Setup

Created a modular ETL project structure separating raw data, processed data, reports, and source code.

---

### Step 2: Metadata Extraction using GDC API

Queried the GDC API to identify available somatic mutation (MAF) files for selected cancer types.

Generated metadata files:

* TCGA-LUAD_d79c2668-6f1e-4736-ac9e-08e7fa58321d.wxs.aliquot_ensemble_masked.maf.gz
* TCGA-BRCA_01d89297-2636-4115-bfcf-993e9523401e.wxs.aliquot_ensemble_masked.maf.gz
* TCGA-COAD_7c3b8f64-0ae8-4428-847e-f10962133716.wxs.aliquot_ensemble_masked.maf.gz

Note: added TCGA-LUAD, TCGA-COAD, TCGA-BRCA in the file names to create cancer_type column in processed file.

---

### Step 3: MAF File Download

Downloaded mutation files corresponding to the selected cancer cohorts.

---

### Step 4: Data Transformation

The transformation pipeline performs:

#### Column Selection

Retained relevant columns:

* Gene symbol
* Chromosome
* Genomic position
* Reference allele
* Alternate allele
* Variant classification
* Sample ID
* cancer_type
* mutation_type

#### Standardization

* Converted gene symbols to uppercase.
* Standardized chromosome naming conventions.

#### Feature Engineering

Created new features:

* `cancer_type`
* `mutation_type` (SNV/INDEL)

#### Dataset Integration

Merged mutation data from multiple cancer types into a single analytics-ready dataset:

```text
combined_mutations.csv
```

---

### Step 5: Data Quality Checks

Implemented automated quality assessment including:

* Missing gene detection
* Missing genomic positions
* Duplicate mutation identification
* Chromosome name validation

Generated:

```text
quality_report.csv
```

---

### Step 6: Dataset Profiling and Summary Statistics

Generated dataset summaries including:

#### Dataset Statistics

* Number of mutation records
* Number of unique samples
* Number of unique genes

#### Mutation Statistics

* Mutation counts per cancer type
* Top mutated genes across all cancers
* Top mutated genes within each cancer type
* Number of mutation types

Generated:

```text
dataset_summary.json
```

## Technologies Used

### Programming

* Python

### Libraries

* Pandas
* NumPy
* Requests
* JSON
* SciPy
* pathlib
* SQLAlchemy
* PostgreQSL

### Data Engineering

* ETL Pipeline Development
* Data Validation
* Data Cleaning
* Data Profiling

### Bioinformatics

* TCGA
* GDC API
* Somatic Mutation Analysis
* Cancer Genomics

### Version Control

* Git
* GitHub

---

### Database Integration

* Load processed mutation data into PostgreSQL using SQLAlchemy.
* Develop analytical SQL queries for mutation exploration.

### Statistical Analysis

Apply statistical methods including:

* Chi-square test
* ANOVA
* Tukey's HSD(Honestly Significant Difference)
* Fisher's exact test
* Mutation burden analysis
  
### Data Visualization

Develop interactive visualizations for:

* Sample distribution in each cancer type
* Mutation distributions
* Top mutated genes (Using mutation count)
* Frequently mutated genes in each cancer (using mutation frequency)
* Cancer-specific mutation landscapes

## Future Work

### Dashboard Development

Build an interactive dashboard using:

* Plotly
* Streamlit

---

## Learning Outcomes

Through this project, I gained hands-on experience in:

* Building end-to-end ETL pipelines
* Working with APIs and JSON data
* Data cleaning and validation
* Cancer genomics data analysis
* Statistical analysis and reporting
* Software engineering best practices using Git and GitHub

---

## Author

**Drishti Singh**

Bioinformatics Scientist | Data Science Enthusiast

Interested in Cancer Genomics, Data Engineering, Machine Learning, and Healthcare Analytics.
# ETL-Pipeline
