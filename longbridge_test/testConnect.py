"""
from longbridge import OpenAPI

# 手动指定凭证

)

# 测试调用：获取账户余额
response = api.account.balance()
print(response)

# testConnect_simple.py
from longbridge import OpenAPI

# ---------- 填入你的 Access Token ----------
REGION = "cn"  # cn / hk / us
 --------------------------------------------------

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
