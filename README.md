# Apple Stock Pipeline Prediction

Welcome to the **Apple Stock Pipeline Prediction** repository!  
This project implements a complete pipeline to **download, store, and analyze** Apple stock data, along with a simple **prediction** for the next day's stock trend.

---

## Features

- **Dockerized PostgreSQL**: Easily set up and manage a PostgreSQL instance with Docker Compose.  
- **Configuration Management**: Use `.env` files to store sensitive information such as database credentials and API keys.  
- **Data Pipeline**: Download, store, and preprocess Apple stock data.  
- **Prediction**: A moving average-based model to estimate the stock trend for the next day.  
- **Reproducible Infrastructure**: A single script (`pipeline.py`) runs all the steps.

---

## Installation & Setup

### 1. Prerequisites

Before starting, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)  
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)  
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)  
- **Git**: [Install Git](https://git-scm.com/downloads/)  

### 2. Start PostgreSQL with Docker Compose

Run the following command to start a PostgreSQL instance:  
```bash
docker compose up -d
```

### 3. Configure Environment Variables

Create a `.env` file based on `example.env`:
```bash
cp example.env .env
```
Change the following settings in the `.env` file:

- Set your **Alpha Vantage API key** (Get it [here](https://www.alphavantage.co/support/#api-key)).
- Set your **PostgreSQL Database URI** by adjusting the user, password, port, and database info as per your `docker-compose.yml`.

For example, if your `docker-compose.yml` file contains the following configuration:

```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: stock_data
    ports:
      - "5432:5432"
```

Your `.env` file should look like:

```env
ALPHA_VANTAGE_API_KEY=your_api_key
DB_URI=postgresql://user:password@localhost:5432/stock_data
```

### 4. Install Dependencies

**Create a Python virtual environment**:  
```bash
python -m venv venv
source venv/bin/activate  # MacOS
venv\Scripts\activate.bat  # Windows
```

**Install dependencies**:  
```bash
pip install -r requirements.txt
```

---

## Run the Pipeline

Execute the following script to run the entire pipeline:

```bash
python pipeline.py
```

---

## Project Structure

```plaintext
📂 apple-stock-pipeline
│── 📂 data/                   # Folder for storing stock data
│── 📂 scripts/                # Python scripts for data processing & modeling
│── .env                       # Environment variables file
│── docker-compose.yml         # PostgreSQL Docker configuration
│── example.env                # Example environment variables
│── pipeline.py                # Main pipeline script
│── README.md                  # Project documentation
│── requirements.txt           # Python dependencies
│── Visualisations.ipnb        # Jupyter notebooks for visualization & analysis
```
---

## Prediction Algorithm Documentation

### Overview

The prediction algorithm analyzes stock price movements using **Simple Moving Averages (SMA)**. It classifies the expected trend as **Positive, Negative, or Stable** based on the relationship between the **5-day SMA (SMA_5)** and **20-day SMA (SMA_20)**.

---

### **Prediction Models**  

#### **1. Original Prediction Model (`predict_stock.py`)**  

This script uses a **Simple Moving Average (SMA)** strategy to classify the expected stock trend as **Positive, Negative, or Stable**.  

#### **Logic:**  
1. **Calculate Moving Averages**  
   - SMA_5 (5-day moving average)  
   - SMA_20 (20-day moving average)  

2. **Predict the Next Day’s Movement**  
   - If `SMA_5 > SMA_20` → **Positive** (Uptrend)  
   - If `SMA_5 < SMA_20` → **Negative** (Downtrend)  
   - If `SMA_5 == SMA_20` → **Stable** (No clear trend)  

#### **Key Assumption:**   
- The algorithm follows a **moving average crossover strategy**, a common technique in technical analysis.  
- A **short-term moving average crossing above** a long-term moving average suggests an **upward trend (bullish)**, while crossing **below** suggests a **downward trend (bearish)**.


---  

#### **2. Alternative Prediction Model (`predict_stock_2.py`)**  

This script extends the original approach by introducing **three different prediction methodologies**:  

1. **SMA-Based Model** (Same as `predict_stock.py`)  
2. **Exponential Moving Average (EMA) Model**  
3. **Percentage Change Model**  

By default, the pipeline applies `predict_stock.py`, but you can switch to `predict_stock_2.py` by modifying the pipeline script to call the alternative model instead. This allows flexibility in choosing the prediction approach without modifying the core pipeline structure.  

#### **Additional Logic in `predict_stock_2.py`:**  

- **EMA-Based Model (Exponential Moving Average):** 
   EMA is similar to SMA but gives more weight to recent prices, making it more sensitive to recent price changes.
   The EMA_5 and EMA_20 work like SMA but react faster to price fluctuations.

  - If `EMA_5 > EMA_20` → **Positive**  
  - If `EMA_5 < EMA_20` → **Negative**  
  - If `EMA_5 == EMA_20` → **Stable**  

- **Percentage Change Model:**  
  - Compares today's closing price with yesterday's.  
  - If the percentage change is above a small threshold (e.g., ±0.1%):  
    - **Positive** if the price increased  
    - **Negative** if the price decreased  
    - **Stable** if the change is within the threshold  

This version of the prediction script (`predict_stock_2.py`) provides a **more comprehensive view** by evaluating stock movement through multiple indicators at once.

## **Stock Data Visualization (`visualizations.ipynb`)**  

The **`visualizations.ipynb`** notebook provides **detailed visual insights** into Apple stock data, including price trends, moving averages, and anomaly detection.

### **Key Sections & Visualizations:**  
1. **Closing Price Trends:** Line chart showing stock price movements over time.  
2. **Moving Averages (SMA & EMA):** Helps identify trends in stock prices.  
3. **Trading Volume Analysis:** Bar charts showing stock trading volumes per year.   
4. **Rolling Statistics:** Moving averages and volatility analysis.  
5. **Machine Learning – Anomaly Detection:** Detects unusual stock price movements using ML techniques.  
6. **Stacked Area Chart:** Visualizes stock price components over time.

### **Usage:**  
Run the notebook in Jupyter:  
```bash
jupyter notebook visualizations.ipynb
```
OR 
Run All Cells in the notebook:
- Open the notebook in your browser.
- Click the "Run All" button at the top of the notebook.

---

## Conclusion

This project provides a **flexible and extensible** pipeline for stock analysis and prediction.  
- **For a quick prediction**, use `predict_stock.py`.  
- **For a more detailed analysis**, use `predict_stock_2.py`.  
- **For in-depth visual analysis**, use `visualization.ipynb`. 