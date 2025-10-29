"""
from longbridge import OpenAPI

# 手动指定凭证
api = OpenAPI(
    app_key="61c12fe09ba7910cd3a65d64a064620d",
    app_secret="d71fab251c59e4a3ce2baa2901bc18a349326dd44fd9cc6792b8592b0da82b3e",
    access_token="m_eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzY5NTE1MDY1LCJpYXQiOjE3NjE3MzkwNTYsImFrIjoiNjFjMTJmZTA5YmE3OTEwY2QzYTY1ZDY0YTA2NDYyMGQiLCJhYWlkIjoyMDc1NDgyNiwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE2MjY5MzIyLCJzaWQiOiJadkY1N1VpbGVNYW56ODdta1JzZVB3PT0iLCJibCI6MywidWwiOjAsImlrIjoibGJfcGFwZXJ0cmFkaW5nXzIwNzU0ODI2In0.j_h0W2IE3UIgpmYesjxPAeydPJmymgeqBzW_-azOPRfJljB4bsvxnBPJe8nMxZ2HQCp5FzwdNiMTU-ri4shmtVDm21PN9vMEcqSrK1mOpAUX55tocokg2AcoF5UVdD9FBlgvV3V5Fa3K80P4HQB1i5bFjOLOx7NrvQViqtQVVcXNmGUiqmbA3jTZxzxAkub1bIcQHZzApaBNGbvs_-hbvfgOLK8fOAOmqnLxe1BbuCsbdFHBBFRLRNxNiGGtwRkYBK3_IL0iXYEfbnFLxga5lMO3dNmeQL-nfmitgAxBUz-OB-aJm5RBdI_Q_QLS4utpm32bz8kPncSx6Dr_V6t950dSyTMrkTFjC3z3-yUKXeph5ht55FTWOwA0zbCSYJGAKbE2PNEoKCZsFtjUJkIQG6D7UIwUubWwuV4uwYs9mBV4O-NPyd1dQLsCN6g8CE9mx4clTkZkylvNuW3-Iog0kEVsqs4Na-33ZGZQyu54gAOGFa9sUj1cKLN-GkVsRO9iSebzGgFxfwI4a-PF5jSJwOSD38CkmUuEjb9cMaS4kDcJIEpA2j6tj8aO49yFBnAuQNAP2Tu3uiOD7inuEdkAOowz2qV5jzUHeucaw6iC2nGillEqdGobg01KBUVAoUIaLFDXKJHzYeZBqM64C01UbmYY2dsnRyV80hB0qHXI0xk",  # 你的 Access Token
    region="hk"  # 根据你页面显示的 Region 填写
)

# 测试调用：获取账户余额
response = api.account.balance()
print(response)

# testConnect_simple.py
from longbridge import OpenAPI

# ---------- 填入你的 Access Token ----------
ACCESS_TOKEN = "m_eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzY5NTE1MDY1LCJpYXQiOjE3NjE3MzkwNTYsImFrIjoiNjFjMTJmZTA5YmE3OTEwY2QzYTY1ZDY0YTA2NDYyMGQiLCJhYWlkIjoyMDc1NDgyNiwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE2MjY5MzIyLCJzaWQiOiJadkY1N1VpbGVNYW56ODdta1JzZVB3PT0iLCJibCI6MywidWwiOjAsImlrIjoibGJfcGFwZXJ0cmFkaW5nXzIwNzU0ODI2In0.j_h0W2IE3UIgpmYesjxPAeydPJmymgeqBzW_-azOPRfJljB4bsvxnBPJe8nMxZ2HQCp5FzwdNiMTU-ri4shmtVDm21PN9vMEcqSrK1mOpAUX55tocokg2AcoF5UVdD9FBlgvV3V5Fa3K80P4HQB1i5bFjOLOx7NrvQViqtQVVcXNmGUiqmbA3jTZxzxAkub1bIcQHZzApaBNGbvs_-hbvfgOLK8fOAOmqnLxe1BbuCsbdFHBBFRLRNxNiGGtwRkYBK3_IL0iXYEfbnFLxga5lMO3dNmeQL-nfmitgAxBUz-OB-aJm5RBdI_Q_QLS4utpm32bz8kPncSx6Dr_V6t950dSyTMrkTFjC3z3-yUKXeph5ht55FTWOwA0zbCSYJGAKbE2PNEoKCZsFtjUJkIQG6D7UIwUubWwuV4uwYs9mBV4O-NPyd1dQLsCN6g8CE9mx4clTkZkylvNuW3-Iog0kEVsqs4Na-33ZGZQyu54gAOGFa9sUj1cKLN-GkVsRO9iSebzGgFxfwI4a-PF5jSJwOSD38CkmUuEjb9cMaS4kDcJIEpA2j6tj8aO49yFBnAuQNAP2Tu3uiOD7inuEdkAOowz2qV5jzUHeucaw6iC2nGillEqdGobg01KBUVAoUIaLFDXKJHzYeZBqM64C01UbmYY2dsnRyV80hB0qHXI0xk"
REGION = "cn"  # cn / hk / us
# --------------------------------------------------

def main():
    # 创建 OpenAPI 实例，只用 Access Token
    api = OpenAPI(
        access_token=ACCESS_TOKEN,
        region=REGION
    )

    try:
        # 测试连接：获取账户信息
        account_info = api.account.get_accounts()
        print("✅ 连接成功！账户信息如下：")
        print(account_info)

        # 测试行情：获取股票实时报价
        symbol = "00700.HK"  # 腾讯港股示例
        quote = api.quote.get_quote(symbol)
        print(f"\n📈 {symbol} 实时行情：")
        print(quote)

    except Exception as e:
        print("❌ 连接失败或获取信息出错：", e)

if __name__ == "__main__":
    main()

"""


from longport.openapi import TradeContext, Config

def main():
    try:
        # 从环境变量读取配置
        config = Config.from_env()

        # 初始化交易上下文
        ctx = TradeContext(config)

        # 查询账户余额
        balance = ctx.account_balance()
        print("账户余额信息：")
        print(balance)

        # 查询账户持仓（示例）
        positions = ctx.account_positions()
        print("\n账户持仓信息：")
        print(positions)

        # 可以加更多操作，例如下单（谨慎使用）
        # order_resp = ctx.place_order(symbol="00700.HK", side="Buy", price=400.0, quantity=1)
        # print("\n下单返回信息：")
        # print(order_resp)

    except Exception as e:
        print("执行出错：", e)

if __name__ == "__main__":
    main()
