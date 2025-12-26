# src/plotting.py
import matplotlib.pyplot as plt
import seaborn as sns


def plot_charts(data, tickers):
    """
    Generates and saves plots for cumulative returns and factor correlations.
    """
    print("🎨 正在繪製圖表...")

    # 圖1: 累積報酬率比較
    plt.figure(figsize=(10, 6))
    cumulative_returns = (1 + data[tickers]).cumprod()
    for col in tickers:
        plt.plot(cumulative_returns.index, cumulative_returns[col], label=col)
    plt.title("Stock Cumulative Returns (2019-2023)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("output/images/cumulative_returns.png")
    plt.close()

    # 圖2: 相關性熱圖 (檢查因子共線性)
    plt.figure(figsize=(8, 6))
    factors = data[["Mkt_RF", "SMB", "HML", "RMW", "CMA"]]
    sns.heatmap(factors.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix of Fama-French 5 Factors")
    plt.tight_layout()
    plt.savefig("output/images/factor_corr.png")
    plt.close()
