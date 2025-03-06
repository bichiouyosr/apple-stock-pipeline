import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def predict_stock_all_models():
    # Load DB URI from .env
    DB_URI = os.getenv("DB_URI")
    engine = create_engine(DB_URI)

    # Load Data
    query = "SELECT * FROM apple_stock ORDER BY date"
    df = pd.read_sql(query, engine)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # Compute Moving Averages (SMA and EMA)
    df["SMA_5"] = df["close"].rolling(window=5).mean()
    df["SMA_20"] = df["close"].rolling(window=20).mean()
    df["EMA_5"] = df["close"].ewm(span=5, adjust=False).mean()
    df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()

    # Get the last row of data (most recent day)
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # Calculate the percentage change
    pct_change = ((last_row["close"] - prev_row["close"]) / prev_row["close"]) * 100

    # Prediction Logic for SMA-based Model
    def predict_sma(row):
        if row["SMA_5"] > row["SMA_20"]:
            return "Positive"
        elif row["SMA_5"] < row["SMA_20"]:
            return "Negative"
        else:
            return "Stable"

    # Prediction Logic for EMA-based Model
    def predict_ema(row):
        if row["EMA_5"] > row["EMA_20"]:
            return "Positive"
        elif row["EMA_5"] < row["EMA_20"]:
            return "Negative"
        else:
            return "Stable"

    # Prediction Logic for Percentage Change Model
    def predict_pct_change(pct_change):
        threshold = 0.1 
        if pct_change > threshold:
            return f"Positive (+{pct_change:.2f}%)"
        elif pct_change < -threshold:
            return f"Negative ({pct_change:.2f}%)"
        else:
            return f"Stable ({pct_change:.2f}%)"

    # Make predictions using all models
    sma_prediction = predict_sma(last_row)
    ema_prediction = predict_ema(last_row)
    pct_change_prediction = predict_pct_change(pct_change)

    # Print the predictions with the updated first line for the predicted next day
    next_day = last_row.name + pd.Timedelta(days=1)
    print(f"The stock price of Apple predicted for the next day: {next_day.date()} is:")

    print("\n1. **SMA-Based Prediction**:")
    print(f"  - SMA_5: {last_row['SMA_5']:.2f}")
    print(f"  - SMA_20: {last_row['SMA_20']:.2f}")
    print(f"  - Prediction: {sma_prediction}")

    print("\n2. **EMA-Based Prediction**:")
    print(f"  - EMA_5: {last_row['EMA_5']:.2f}")
    print(f"  - EMA_20: {last_row['EMA_20']:.2f}")
    print(f"  - Prediction: {ema_prediction}")

    print("\n3. **Percentage Change Prediction**:")
    print(f"  - Today's Close: {last_row['close']}")
    print(f"  - Yesterday's Close: {prev_row['close']}")
    print(f"  - Percentage Change: {pct_change:.2f}%")
    print(f"  - Prediction: {pct_change_prediction}")

