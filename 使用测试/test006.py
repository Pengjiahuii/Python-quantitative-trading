from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

# 订阅苹果股票行情
contract = Stock('AAPL', 'SMART', 'USD')
ticker = ib.reqMktData(contract)

ib.sleep(2)
print(f"AAPL 实时报价: {ticker.last}, 买价: {ticker.bid}, 卖价: {ticker.ask}")
