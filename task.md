### 1. 選股與特徵整理 (Stock Selection & Characteristics)

題目要求擴充至 10 檔。消費與零售板塊通常分為「必需性消費 (Consumer Staples)」與「非必需性消費 (Consumer Discretionary)」。建議混合選取，以利於在模型分析時觀察不同的因子曝險。

**建議的 10 檔股票組合 (Ticker):**

| 公司 (Ticker) | 產業分類 | 規模 (Size) | 估值特徵 (Value/Growth) | 預期屬性 |
| --- | --- | --- | --- | --- |
| **Walmart (WMT)** | 必需消費/超市 | Mega Cap | Value | 低波動，防禦型 |
| **Costco (COST)** | 必需消費/量販 | Large Cap | Growth at Reasonable Price | 高營運效率 |
| **McDonald's (MCD)** | 非必需/餐飲 | Large Cap | Value/Stable | 全球化，現金流穩 |
| **Nike (NKE)** | 非必需/服飾 | Large Cap | Growth | 品牌溢價高 |
| **Starbucks (SBUX)** | 非必需/餐飲 | Large Cap | Growth/Mature | 週期性較強 |
| **Target (TGT)** | 非必需/百貨 | Large Cap | Value | 較高波動 |
| **Home Depot (HD)** | 非必需/家居 | Large Cap | Cyclical | 房市連動強 |
| **Coca-Cola (KO)** | 必需消費/飲料 | Mega Cap | Value | 高股息，極低 Beta |
| **PepsiCo (PEP)** | 必需消費/飲料 | Mega Cap | Value | 穩健防禦 |
| **Amazon (AMZN)*** | 非必需/電商 | Mega Cap | High Growth | **特異點**：兼具科技屬性 |

> **註**：加入 Amazon 是為了增加對比度。它是零售商，但財務特徵（低帳面市值比、高投資）與傳統零售（如 Walmart）截然不同，這在 FF3 和 FF5 模型中會產生很有趣的差異。

---

### 2. 模型理論架構 (Theoretical Framework)

報告中需使用 LaTeX 清晰呈現數學模型。

#### A. CAPM (Capital Asset Pricing Model)

**核心概念：** 只考慮「市場風險」。


* : 資產回報率
* : 無風險利率
* : 市場回報率
* **解釋力限制：** 無法解釋為什麼小型股或價值股長期回報較高（異常報酬  存在）。

#### B. Fama-French 三因子 (FF3)

**核心概念：** 新增「規模」與「價值」效應。


* **SMB (Small Minus Big):** 規模因子。零售巨頭（如 WMT）通常在此係數為負（Big）。
* **HML (High Minus Low):** 價值因子（帳面市值比 B/M）。傳統零售（KO, MCD）通常為正（Value）；高成長股（AMZN）通常為負。

#### C. Fama-French 五因子 (FF5)

**核心概念：** FF3 仍無法解釋為什麼有些低 B/M 的股票（如高獲利科技或強勢零售）回報依然高，因此加入「獲利能力」與「投資風格」。


* **RMW (Robust Minus Weak):** 獲利能力因子。Costco 或 McDonald's 這種高護城河、高獲利公司，RMW 係數應顯著為正。
* **CMA (Conservative Minus Aggressive):** 投資因子。過度擴張（Aggressive Investment）的公司回報通常較低。成熟零售商通常投資保守（Conservative），CMA 為正；Amazon 若在大舉擴張期，CMA 可能為負。

---

### 3. 模型比較與差異分析 (分析重點)

這是報告的核心，你需要回答以下問題（建議用數據佐證）：

1. **CAPM 的不足：**
* 在 CAPM 下，你可能會發現傳統零售股（如 KO）的 （截距項）顯著不為 0，或  較低。這代表單一市場因子無法完全解釋其波動。


2. **FF3 的改進 (SMB/HML)：**
* **HML 的作用：** 對於 Walmart 或 Target 這類傳統零售商，加入 HML 後，模型的解釋力 () 應該會提升。因為它們的表現與「價值股」週期高度相關。
* **SMB 的作用：** 由於你選的都是大型股 (Large Cap)， 係數應該普遍為負（Big size），這驗證了它們是大盤股的屬性。


3. **FF5 的全面性 (RMW/CMA)：**
* **RMW 關鍵點：** 消費零售業非常看重「營運效率」與「利潤率」。像 Nike 或 Costco 這種高 ROE 的公司，FF3 可能會低估其預期回報，而 FF5 的 RMW 因子應該能解釋這部分超額報酬。
* **CMA 關鍵點：** 用來區分「穩健擴張」與「激進燒錢」。



---

### 4. 實作策略：工程師視角 (The Implementation)

為了拿到「報告品質」與「額外內容」的分數，建議直接寫 Python Script 跑回歸分析，產出真實圖表。

**工具推薦：**

* `pandas-datareader`: 直接抓取 Fama-French 因子的官方數據。
* `yfinance`: 抓取個股股價。
* `statsmodels`: 進行 OLS 線性回歸分析。

**Python 程式碼邏輯 (你可以直接參考並實作)：**

```python
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 1. 設定時間範圍
start_date = '2019-01-01'
end_date = '2023-12-31'

# 2. 獲取 Fama-French 5因子數據 (來自 Ken French Library)
# dataset name: 'F-F_Research_Data_5_Factors_2x3_daily'
ff5 = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench', start_date, end_date)[0]
# 轉換百分比為小數
ff5 = ff5 / 100
# 重新命名以便識別 (Mkt-RF, SMB, HML, RMW, CMA, RF)

# 3. 獲取股票數據
tickers = ['WMT', 'COST', 'MCD', 'NKE', 'SBUX', 'TGT', 'HD', 'KO', 'PEP', 'AMZN']
stock_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
stock_returns = stock_data.pct_change().dropna()

# 4. 合併數據 (對齊日期)
data = pd.merge(stock_returns, ff5, left_index=True, right_index=True)

# 5. 迴歸分析函式
def run_regression(ticker, model_type='CAPM'):
    Y = data[ticker] - data['RF'] # 超額報酬
    
    if model_type == 'CAPM':
        X = data[['Mkt-RF']]
    elif model_type == 'FF3':
        X = data[['Mkt-RF', 'SMB', 'HML']]
    elif model_type == 'FF5':
        X = data[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
    
    X = sm.add_constant(X) # 加入截距項 Alpha
    model = sm.OLS(Y, X).fit()
    return model

# 6. 範例：分析 Walmart (WMT)
model_ff5 = run_regression('WMT', 'FF5')
print(model_ff5.summary())

# TODO: 迴圈跑完所有股票，將 Alpha, Beta, R-squared 存入 DataFrame 製作比較表

```

---

### 5. 報告撰寫架構 (Report Outline)

為了符合評分標準，請依照此架構撰寫：

**封面**

* 題目、組別/姓名、學號

**一、緒論 (Introduction)**

* 研究動機：為何選擇 M-3 消費零售？（民生必需、抗通膨屬性、疫情後的復甦）。
* 選股邏輯：列出 10 檔股票清單與分類。

**二、模型理論 (Methodology)**

* (用 LaTeX 列出三個模型的公式)
* 簡述每個因子代表的經濟意義。

**三、數據分析 (Data Analysis) [重點]**

* **敘述性統計：** 10 檔股票的平均報酬、標準差（風險）。
* **模型回歸結果比較表：**
* 做一個大表：列出 10 檔股票在 FF5 下的各因子係數 () 與 。
* **關鍵發現：**
* *範例寫法：* 「如表 1 所示，Costco 的 RMW 係數顯著為正 (t-stat > 2)，證實了其高獲利能力的特徵對於定價有顯著解釋力，這是 CAPM 無法捕捉的。」
* *範例寫法：* 「Amazon 的 HML 係數為負，顯示其具有成長股特徵，與 Walmart (HML > 0) 形成強烈對比。」





**四、解釋力總結 (Results & Discussion)**

* **CAPM vs FF3 vs FF5：** 比較 Adjusted 。通常 FF5 在零售業的解釋力會最高。
* **因子有效性分析：** 在消費零售板塊，哪一個因子最顯著？（通常 Market 和 HML 最顯著，CMA 可能較不顯著）。

**五、結論 (Conclusion)**

* 總結模型優劣。
* 投資建議：基於模型分析，若要建構防禦型組合，應選擇 HML 和 RMW 高的股票（如 KO, PEP）。

**附錄 (Appendix)**

* 附上你的 Python 程式碼片段（證明你是自己做的，符合工程師風格）。

---

### 6. 給使用者的下一步 (Next Steps)

這是一個標準的計量金融分析流程。你需要做的下一步是：

1. **確認環境**：你有安裝 Python 環境嗎？(需要 `pip install yfinance pandas-datareader statsmodels matplotlib`)
2. **執行分析**：你需要我提供**完整的 Python 腳本**嗎？我可以寫一個腳本，執行後直接輸出這 10 檔股票的比較 CSV 和圖表，你只需要截圖貼進報告即可。
3. **LaTeX 支援**：如果你不熟悉 LaTeX 語法，我可以提供公式的原始碼供你直接複製。

請問你想先從**產出 Python 分析腳本**開始嗎？
