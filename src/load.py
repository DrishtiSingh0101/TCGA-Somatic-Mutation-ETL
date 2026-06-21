import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://drishti:postgresql1stpw@localhost:5432/cancerdb"
)

df = pd.read_csv(
    "data/processed/combined_mutations.csv"
)

print(f"Loading {len(df)} records...")

df.to_sql(
    "mutations",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Data loaded successfully into PostgreSQL!")
