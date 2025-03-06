import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL Connection
DB_URI = "postgresql://yosr:yosr@localhost:5432/stock_data"
engine = create_engine(DB_URI)

# Load CSV
df = pd.read_csv("apple_stock_data.csv", parse_dates=["Unnamed: 0"])
df.rename(columns={"Unnamed: 0": "date"}, inplace=True)

# Define Schema & Upload Data
#df.to_sql("apple_stock", engine, if_exists="replace", index=False)
print(df.info())
print("✅ Data uploaded to PostgreSQL!")

