from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

contract = Stock('AAPL', 'SMART', 'USD')
order = MarketOrder('BUY', 1)
trade = ib.placeOrder(contract, order)

ib.sleep(2)
print(trade)