import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_data():
    # Load DB URI from .env
    DB_URI = os.getenv("DB_URI")
    engine = create_engine(DB_URI)

    # Load CSV
    df = pd.read_csv("data/apple_stock_data.csv", parse_dates=["Unnamed: 0"])
    df.rename(columns={"Unnamed: 0": "date"}, inplace=True)

    # Define Schema & Upload Data
    df.to_sql("apple_stock", engine, if_exists="replace", index=False)
    print("✅ Data uploaded to PostgreSQL!")


