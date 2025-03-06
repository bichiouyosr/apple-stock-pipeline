import pandas as pd
from sqlalchemy import create_engine

# Connect to Database
DB_URI = "postgresql://yosr:yosr@localhost:5432/stock_data"
engine = create_engine(DB_URI)

# Load Data
query = "SELECT * FROM apple_stock ORDER BY date"
df = pd.read_sql(query, engine)
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# Compute Moving Averages for the last available day
df["SMA_5"] = df["close"].rolling(window=5).mean()
df["SMA_20"] = df["close"].rolling(window=20).mean()

# Get the last row of data (most recent day)
last_row = df.iloc[-1]

# Prediction Logic for the next day
def predict_next_day(row):
    if row["SMA_5"] > row["SMA_20"]:
        return "Positive"
    elif row["SMA_5"] < row["SMA_20"]:
        return "Negative"
    else:
        return "Stable"

# Predict next day's movement based on the last available day
prediction = predict_next_day(last_row)
print(f"Prediction for next day: {prediction}")
