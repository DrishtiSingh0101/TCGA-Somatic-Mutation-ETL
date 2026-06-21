from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://drishti:postgresql1stpw@localhost:5432/cancerdb"
)

try:
	with engine.connect() as conn:
		print("Successfully connected to postgresql!")
except exception as e:
		print("Connection failed")
		print(e)
