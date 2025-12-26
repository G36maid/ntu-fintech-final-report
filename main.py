# main.py
import os
from src.data_fetching import fetch_data
from src.analysis import run_regressions, save_latex_tables
from src.plotting import plot_charts

# 設定參數
START_DATE = "2019-01-01"
END_DATE = "2023-12-31"
TICKERS = ["WMT", "COST", "MCD", "NKE", "SBUX", "TGT", "HD", "KO", "PEP", "AMZN"]

# 輸出路徑
os.makedirs("output/tables", exist_ok=True)
os.makedirs("output/images", exist_ok=True)


def main():
    """
    Main function to run the financial analysis pipeline.
    """
    data = fetch_data(TICKERS, START_DATE, END_DATE)
    if data is not None:
        results = run_regressions(data, TICKERS)
        save_latex_tables(results)
        plot_charts(data, TICKERS)
        print("✅ 完成！所有輸出的 .tex 和 .png 檔案已儲存於 output/ 目錄。")


if __name__ == "__main__":
    main()
