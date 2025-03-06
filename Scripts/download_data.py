# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
URL = "https://www.alphavantage.co/query"

def download_data():
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "AAPL",
        "apikey": API_KEY,
        "outputsize": "full"
    }
    response = requests.get(URL, params=params)
    data = response.json()

    # Parse the response
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Create a 'data' directory if it doesn't exist
    os.makedirs("Data", exist_ok=True)
    
    # Save to CSV inside the 'data' folder
    file_path = os.path.join("Data", "apple_stock_data.csv")
    df.to_csv(file_path)
    print(f"✅ Data downloaded and saved at {file_path}!")
