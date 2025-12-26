# scripts/download_data.py
import os
from src.data_fetching import fetch_data

# 設定參數
START_DATE = "2019-01-01"
END_DATE = "2023-12-31"
TICKERS = ["WMT", "COST", "MCD", "NKE", "SBUX", "TGT", "HD", "KO", "PEP", "AMZN"]
OUTPUT_DIR = "data/raw"


def main():
    """
    Downloads and saves the financial data.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = fetch_data(TICKERS, START_DATE, END_DATE)
    if data is not None:
        output_path = os.path.join(OUTPUT_DIR, "financial_data.csv")
        data.to_csv(output_path)
        print(f"✅ 數據已儲存至 {output_path}")


if __name__ == "__main__":
    main()
