from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

contract = Stock('AAPL', 'SMART', 'USD')
order = MarketOrder('BUY', 1)
trade = ib.placeOrder(contract, order)

ib.sleep(1)
print(trade)
