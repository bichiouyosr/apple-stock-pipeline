# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
URL = "https://www.alphavantage.co/query"

# Fetch stock data
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": API_KEY,
    "outputsize": "full"
}
response = requests.get(URL, params=params)
data = response.json()

# Parse response
df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
df.columns = ["open", "high", "low", "close", "volume"]
df.index = pd.to_datetime(df.index)
df = df.sort_index()

# Save to CSV
df.to_csv("apple_stock_data.csv")
print("✅ Data downloaded and saved!")

