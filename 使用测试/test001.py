from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

print(ib.reqCurrentTime())  # 测试连接是否成功
ib.disconnect()

