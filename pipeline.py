import os
import subprocess
import sys
from Scripts.download_data import download_data
from Scripts.upload_data import upload_data
from Scripts.predict_stock import predict_stock
from Scripts.all_in_one import predict_stock_all_models

def run():
    """
    This function runs the entire pipeline:
    - Downloads Apple stock data
    - Uploads it to PostgreSQL
    - Runs the prediction model
    """
    try:
        # Step 1: Download the stock data
        print("Step 1: Downloading Apple stock data...")
        download_data()

        # Step 2: Upload the data to PostgreSQL
        print("Step 2: Uploading data to PostgreSQL...")
        upload_data()

        # Step 3: Run the predictive model
        print("Step 3: Running prediction model...")
        #predict_stock()
        predict_stock_all_models()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
