from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# 打印账户摘要
for item in ib.accountSummary():
    print(item)
