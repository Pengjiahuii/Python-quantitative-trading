from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

# 打印账户摘要
for item in ib.accountSummary():
    print(item)