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
│── 📂 data/                   # Downloaded raw data
│── 📂 scripts/                # Python scripts
│   │── download_data.py       # Fetches stock data from Alpha Vantage
│   │── upload_data.py         # Stores data in PostgreSQL
│   │── predict_stock.py       # Predicts the next day's trend
│── .env                       # Environment variables
│── pipeline.py                # Runs the entire pipeline
│── requirements.txt           # Python dependencies
│── README.md                  # This README file
│── docker-compose.yml         # PostgreSQL Docker configuration
│── example.env                # Example environment file
```

---

## Prediction Algorithm Documentation

### Overview

The prediction algorithm analyzes stock price movements using **Simple Moving Averages (SMA)**. It classifies the expected trend as **Positive, Negative, or Stable** based on the relationship between the **5-day SMA (SMA_5)** and **20-day SMA (SMA_20)**.

---

### Steps & Logic 

1. **Load Stock Data**  
   - Retrieve historical stock prices from a PostgreSQL database.  
   - Convert the `date` column to a datetime format and set it as the index.

2. **Calculate Moving Averages**  
   - Compute **SMA_5** (5-day moving average) → Short-term trend indicator.  
   - Compute **SMA_20** (20-day moving average) → Long-term trend indicator.

3. **Determine Trend Based on SMA Comparison**  
   - **If SMA_5 > SMA_20** → **"Positive"** (Short-term uptrend)  
   - **If SMA_5 < SMA_20** → **"Negative"** (Short-term downtrend)  
   - **If SMA_5 == SMA_20** → **"Stable"** (No clear trend)

4. **Predict Next Day's Movement**  
   - The most recent SMA values are used to classify the expected trend.  
   - The prediction is printed as **"Positive", "Negative", or "Stable"**.

---

### **Key Assumption**  

- The algorithm follows a **moving average crossover strategy**, a common technique in technical analysis.  
- A **short-term moving average crossing above** a long-term moving average suggests an **upward trend (bullish)**, while crossing **below** suggests a **downward trend (bearish)**.

