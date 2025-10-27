from ib_insync import IB, Stock
import time

# --------------------------
# 1️⃣ 股票列表
# --------------------------
symbols = [
    "AAPL","MSFT","AMZN","GOOGL","GOOG","TSLA","NVDA","META","JPM","UNH",
    "V","MA","PG","HD","BAC","XOM","DIS","PFE","KO","CVX",
    "MRK","ABT","WMT","NFLX","INTC","ORCL","NKE","TMO","MCD","MDT",
    "CSCO","VZ","ADBE","CRM","BMY","LLY","QCOM","ACN","AMGN","HON",
    "COST","IBM","AVGO","TXN","AMT","UPS","PYPL","UNP","SBUX","MMM",
    "INTU","CAT","LIN","GS","SCHW","RTX","SPGI","T","ADP","BLK",
    "GILD","C","PLD","DE","NOW","ISRG","MDLZ","FIS","GE","MO",
    "CB","BKNG","ZTS","FISV","LRCX","ITW","CL","EL","SO","ANTM",
    "ADI","ATVI","SYK","CI","MS","DHR","GM","BD","MU","TGT",
    "DUK","PEP","MMC","SHW","AON","EQIX","AXP","EW","SLB","CSX",
    "FCX","ECL","HCA","TFC","APD","COF","GPN","PGR","KMB","SYY",
    "VRTX","OXY","NEM","LLY","MMM","HLT","ETN","ICE","ADI","MET",
    "PXD","TEL","HES","MCO","SRE","IT","VLO","KLAC","AIG","STZ",
    "ELV","CTAS","WBA","CPB","MAR","HOG","FITB","MRNA","ZBH","DD",
    "ADM","GIS","KHC","EW","MNST","TRV","F","D","ROP","A","LMT",
    "VTR","PSA","EXC","AFL","PAYX","TEL","AEE","NOC","PNW","DXC",
    "APH","JNJ","BK","AAL","PNC","RMD","WRB","ALGN","K","KR","ETR",
    "ATO","CCI","RSG","CF","WM","CSCO","PFG","HSY","DOW","KMI",
    "EOG","WEC","TEL","PSA","WMB","DTE","XEL","PEG","ETN","AEP"
]

# --------------------------
# 2️⃣ 连接 IBKR 模拟账户
# --------------------------
ib = IB()
connected = ib.connect('127.0.0.1', 7497, clientId=10, timeout=20)
if not connected:
    print("❌ 连接 TWS 失败，请确认 TWS 已打开，API 设置已允许")
    exit()

# --------------------------
# 3️⃣ 使用延迟行情（避免收费/报错）
# --------------------------
ib.reqMarketDataType(3)  # 3 = Delayed

# --------------------------
# 4️⃣ 创建合约并订阅行情
# --------------------------
contracts = [Stock(sym, 'SMART', 'USD') for sym in symbols]
for c in contracts:
    ib.reqMktData(c, '', False, False)
    time.sleep(0.1)  # 避免短时间内请求过多

print(f"✅ 已关注 {len(symbols)} 支股票，TWS Market Watch 可见")

# --------------------------
# 5️⃣ 保持连接，方便查看行情
# --------------------------
try:
    ib.run()
except KeyboardInterrupt:
    print("已停止关注并退出")
    ib.disconnect()
