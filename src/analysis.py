# src/analysis.py
import pandas as pd
import statsmodels.api as sm


def run_regressions(data, tickers):
    """
    Runs CAPM, Fama-French 3-factor, and Fama-French 5-factor regressions.
    """
    results_list = []
    print("⚡ 正在執行回歸分析 (CAPM / FF3 / FF5)...")

    for ticker in tickers:
        Y = data[ticker] - data["RF"]
        models = {
            "CAPM": ["Mkt_RF"],
            "FF3": ["Mkt_RF", "SMB", "HML"],
            "FF5": ["Mkt_RF", "SMB", "HML", "RMW", "CMA"],
        }
        row_data = {"Ticker": ticker}

        for name, factors in models.items():
            X = data[factors]
            X = sm.add_constant(X)
            model = sm.OLS(Y, X).fit()
            row_data[f"{name}_R2"] = model.rsquared_adj

            if name == "FF5":
                row_data["Beta"] = model.params["Mkt_RF"]
                row_data["SMB"] = model.params["SMB"]
                row_data["HML"] = model.params["HML"]
                row_data["RMW"] = model.params["RMW"]
                row_data["CMA"] = model.params["CMA"]
                row_data["Alpha"] = model.params["const"]
        results_list.append(row_data)

    return pd.DataFrame(results_list)


def save_latex_tables(df_results):
    """
    Saves regression results to LaTeX tables.
    """
    print("📝 正在生成 LaTeX 表格...")

    # 表1: 模型解釋力比較 (R-squared)
    r2_cols = ["Ticker", "CAPM_R2", "FF3_R2", "FF5_R2"]
    df_r2 = df_results[r2_cols].copy()
    # Rename columns to LaTeX-safe names
    df_r2.columns = ["Ticker", "CAPM $R^2$", "FF3 $R^2$", "FF5 $R^2$"]
    for col in df_r2.columns[1:]:
        df_r2[col] = df_r2[col].apply(lambda x: f"{x:.4f}")

    latex_r2 = df_r2.to_latex(
        index=False,
        caption="三種模型之調整後 R-squared 比較",
        label="tab:r2_compare",
        position="htbp",
        escape=False,
    )
    with open("output/tables/r2_comparison.tex", "w") as f:
        f.write(latex_r2)

    # 表2: FF5 因子係數表
    factor_cols = ["Ticker", "Alpha", "Beta", "SMB", "HML", "RMW", "CMA"]
    df_factors = df_results[factor_cols].copy()
    for col in factor_cols[1:]:
        df_factors[col] = df_factors[col].apply(lambda x: f"{x:.4f}")

    latex_factors = df_factors.to_latex(
        index=False,
        caption="Fama-French 五因子模型係數估計",
        label="tab:ff5_params",
        position="htbp",
    )
    with open("output/tables/ff5_factors.tex", "w") as f:
        f.write(latex_factors)
