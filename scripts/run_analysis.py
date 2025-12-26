# scripts/run_analysis.py
import os
import pandas as pd
from src.analysis import run_regressions, save_latex_tables
from src.plotting import plot_charts

# 設定參數
TICKERS = ["WMT", "COST", "MCD", "NKE", "SBUX", "TGT", "HD", "KO", "PEP", "AMZN"]
DATA_PATH = "data/raw/financial_data.csv"
OUTPUT_DIR_TABLES = "output/tables"
OUTPUT_DIR_IMAGES = "output/images"


def main():
    """
    Runs the financial analysis pipeline.
    """
    os.makedirs(OUTPUT_DIR_TABLES, exist_ok=True)
    os.makedirs(OUTPUT_DIR_IMAGES, exist_ok=True)

    if not os.path.exists(DATA_PATH):
        print(f"⚠️ 數據文件不存在: {DATA_PATH}")
        print("請先運行 'python -m scripts.download_data' 來下載數據。")
        return

    data = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    results = run_regressions(data, TICKERS)
    save_latex_tables(results)
    plot_charts(data, TICKERS)
    print("✅ 分析完成！所有輸出的 .tex 和 .png 檔案已儲存於 output/ 目錄。")


if __name__ == "__main__":
    main()
