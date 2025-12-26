# src/data_fetching.py
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf


def fetch_data(tickers, start_date, end_date):
    """
    Fetches stock prices and Fama-French 5 factors data.
    """
    print("🚀 正在抓取數據...")

    # 1. 抓取股價
    raw_data = yf.download(tickers, start=start_date, end=end_date)
    if "Adj Close" in raw_data.columns:
        prices = raw_data["Adj Close"]
    else:
        print("⚠️ 'Adj Close' not found. Using 'Close' instead.")
        prices = raw_data["Close"]
    
    stock_returns = prices.pct_change().dropna()

    # 2. 抓取 Fama-French 5因子
    try:
        ff5 = web.DataReader(
            "F-F_Research_Data_5_Factors_2x3_daily", "famafrench", start_date, end_date
        )[0]
        ff5 = ff5 / 100
        ff5.rename(columns={"Mkt-RF": "Mkt_RF"}, inplace=True)
    except Exception as e:
        print(f"⚠️ 無法下載 Fama-French 數據: {e}")
        return None

    # 3. 合併數據
    data = pd.merge(stock_returns, ff5, left_index=True, right_index=True)
    return data
