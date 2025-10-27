from ib_insync import *
import pandas as pd
import time
from datetime import datetime, time as dt_time, timedelta
import logging
import pytz

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


class AllDayTradingStrategy:
    def __init__(self, ib_instance, account_value=10000):
        self.ib = ib_instance
        self.account_value = account_value
        self.risk_per_trade = 0.01  # 单笔风险1%
        self.max_positions = 3  # 最大持仓数量
        self.positions = {}  # 当前持仓 {symbol: {entry_price, stop_loss, quantity, contract}}

        # 交易参数 - 根据不同时段调整
        self.trading_sessions = {
            'pre_market': {'profit_target': 0.02, 'stop_loss_pct': 0.015},  # 盘前：2%目标，1.5%止损
            'regular': {'profit_target': 0.015, 'stop_loss_pct': 0.01},  # 盘中：1.5%目标，1%止损
            'after_hours': {'profit_target': 0.025, 'stop_loss_pct': 0.02},  # 盘后：2.5%目标，2%止损
            'night': {'profit_target': 0.03, 'stop_loss_pct': 0.025}  # 夜盘：3%目标，2.5%止损
        }

        # 交易时段定义（美东时间）
        self.session_times = {
            'pre_market': (dt_time(4, 0), dt_time(9, 30)),  # 盘前：4:00 - 9:30
            'regular': (dt_time(9, 30), dt_time(16, 0)),  # 盘中：9:30 - 16:00
            'after_hours': (dt_time(16, 0), dt_time(20, 0)),  # 盘后：16:00 - 20:00
            'night': (dt_time(20, 0), dt_time(4, 0))  # 夜盘：20:00 - 次日4:00
        }

        # 时区设置
        self.ny_tz = pytz.timezone('America/New_York')
        self.local_tz = pytz.timezone('Asia/Shanghai')  # 根据您的位置调整

        # 监控列表 - 包含不同波动性的标的
        self.watchlist = [
            'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'TSLA',  # 大盘股
            'SPY', 'QQQ', 'IWM',  # ETF
            'UVXY', 'SQQQ', 'TQQQ'  # 高波动ETF
        ]
        self.contracts = {}

        # 性能统计
        self.trade_history = []

    def get_current_ny_time(self):
        """获取当前纽约时间"""
        utc_now = pytz.utc.localize(datetime.utcnow())
        ny_time = utc_now.astimezone(self.ny_tz)
        return ny_time

    def get_current_session(self):
        """获取当前交易时段"""
        ny_time = self.get_current_ny_time()
        current_time = ny_time.time()

        for session, (start, end) in self.session_times.items():
            if session != 'night':
                if start <= current_time < end:
                    return session
            else:  # 夜盘特殊处理（跨天）
                if current_time >= start or current_time < end:
                    return session
        return 'closed'

    def is_trading_hours(self):
        """检查是否在交易时间内"""
        current_session = self.get_current_session()
        return current_session != 'closed'

    def get_session_params(self):
        """获取当前时段的交易参数"""
        session = self.get_current_session()
        return self.trading_sessions.get(session, {'profit_target': 0.02, 'stop_loss_pct': 0.015})

    def setup_contracts(self):
        """设置合约详情"""
        logger.info("设置合约...")
        for symbol in self.watchlist:
            try:
                contract = Stock(symbol, 'SMART', 'USD')
                # 验证合约
                details = self.ib.reqContractDetails(contract)
                if details:
                    self.contracts[symbol] = contract
                    logger.info(f"合约验证成功: {symbol}")
                else:
                    logger.warning(f"合约验证失败: {symbol}")
            except Exception as e:
                logger.error(f"设置合约失败 {symbol}: {e}")

    def calculate_position_size(self, entry_price, stop_loss_price):
        """根据风险计算仓位大小"""
        try:
            risk_per_share = abs(entry_price - stop_loss_price)
            if risk_per_share <= 0:
                return 0

            risk_amount = self.account_value * self.risk_per_trade
            shares = risk_amount / risk_per_share

            # 限制最大仓位
            max_shares_by_capital = (self.account_value * 0.1) / entry_price  # 最多10%资金
            shares = min(shares, max_shares_by_capital)

            return int(max(1, shares))  # 至少1股

        except Exception as e:
            logger.error(f"计算仓位失败: {e}")
            return 0

    def get_current_price(self, symbol):
        """获取当前价格"""
        try:
            if symbol in self.contracts:
                contract = self.contracts[symbol]
                ticker = self.ib.reqMktData(contract, '', False, False)
                self.ib.sleep(1)  # 等待数据更新

                # 优先使用最后成交价，如果没有则使用中间价
                if ticker.last > 0:
                    return ticker.last
                elif ticker.bid > 0 and ticker.ask > 0:
                    return (ticker.bid + ticker.ask) / 2
                else:
                    return 0
        except Exception as e:
            logger.error(f"获取价格失败 {symbol}: {e}")
        return 0

    def get_historical_volatility(self, symbol, days=20):
        """计算历史波动率"""
        try:
            contract = self.contracts[symbol]
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr=f'{days} D',
                barSizeSetting='1 day',
                whatToShow='TRADES',
                useRTH=False,
                formatDate=1
            )

            if len(bars) > 1:
                closes = [bar.close for bar in bars]
                returns = []
                for i in range(1, len(closes)):
                    daily_return = (closes[i] - closes[i - 1]) / closes[i - 1]
                    returns.append(daily_return)

                import numpy as np
                volatility = np.std(returns) * np.sqrt(252)  # 年化波动率
                return volatility

        except Exception as e:
            logger.error(f"计算波动率失败 {symbol}: {e}")

        return 0.3  # 默认波动率

    def generate_trading_signals(self, symbol):
        """生成交易信号 - 多策略组合"""
        try:
            current_price = self.get_current_price(symbol)
            if current_price <= 0:
                return False, 0, 0

            # 获取不同时间周期的数据
            timeframes = ['5 mins', '15 mins', '1 hour']
            signals = []

            for timeframe in timeframes:
                contract = self.contracts[symbol]
                bars = self.ib.reqHistoricalData(
                    contract,
                    endDateTime='',
                    durationStr='2 D',
                    barSizeSetting=timeframe,
                    whatToShow='TRADES',
                    useRTH=False,
                    formatDate=1
                )

                if len(bars) > 20:
                    df = util.df(bars)

                    # 策略1: 突破策略
                    resistance = df['high'].iloc[-20:-1].max()
                    support = df['low'].iloc[-20:-1].min()

                    if current_price > resistance:
                        signals.append(1)  # 做多信号
                    elif current_price < support:
                        signals.append(-1)  # 做空信号
                    else:
                        signals.append(0)  # 无信号

                    # 策略2: 均值回归（RSI）
                    if len(df) > 14:
                        delta = df['close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi = 100 - (100 / (1 + rs))

                        current_rsi = rsi.iloc[-1]
                        if current_rsi < 30:
                            signals.append(1)  # 超卖，做多
                        elif current_rsi > 70:
                            signals.append(-1)  # 超买，做空

            # 综合信号
            if signals.count(1) > signals.count(-1):
                session_params = self.get_session_params()
                stop_loss_price = current_price * (1 - session_params['stop_loss_pct'])
                return True, current_price, stop_loss_price

        except Exception as e:
            logger.error(f"生成信号失败 {symbol}: {e}")

        return False, 0, 0

    def place_buy_order(self, symbol, quantity, price):
        """下买入订单"""
        try:
            contract = self.contracts[symbol]
            current_session = self.get_current_session()

            # 根据时段选择订单类型
            if current_session == 'regular':
                order = LimitOrder('BUY', quantity, round(price * 1.001, 2))  # 提高一点价格确保成交
            else:
                order = LimitOrder('BUY', quantity, round(price * 1.002, 2))  # 非主流时段提高价格

            order.transmit = True

            trade = self.ib.placeOrder(contract, order)
            logger.info(f"提交订单: {symbol}, 数量: {quantity}, 价格: {order.lmtPrice}")

            # 等待订单状态更新
            for i in range(10):
                if trade.orderStatus.status in ['Filled', 'Cancelled', 'ApiCancelled']:
                    break
                self.ib.sleep(1)

            if trade.orderStatus.status == 'Filled':
                fill_price = float(trade.orderStatus.avgFillPrice)
                session_params = self.get_session_params()
                stop_loss_price = fill_price * (1 - session_params['stop_loss_pct'])

                # 记录持仓
                self.positions[symbol] = {
                    'entry_price': fill_price,
                    'stop_loss': stop_loss_price,
                    'quantity': quantity,
                    'contract': contract,
                    'entry_time': self.get_current_ny_time(),
                    'session': current_session,
                    'profit_target': session_params['profit_target']
                }

                logger.info(f"订单成交: {symbol}, 数量: {quantity}, 价格: {fill_price:.2f}")
                return True
            else:
                self.ib.cancelOrder(order)
                logger.warning(f"订单未成交: {symbol}, 状态: {trade.orderStatus.status}")
                return False

        except Exception as e:
            logger.error(f"下单失败 {symbol}: {e}")
            return False

    def check_exit_conditions(self, symbol):
        """检查出场条件"""
        if symbol not in self.positions:
            return

        position = self.positions[symbol]
        current_price = self.get_current_price(symbol)

        if current_price <= 0:
            return

        entry_price = position['entry_price']
        current_pnl_pct = (current_price - entry_price) / entry_price
        stop_loss_price = position['stop_loss']
        profit_target = position['profit_target']

        exit_reason = None

        # 条件1: 止损
        if current_price <= stop_loss_price:
            exit_reason = f"止损 ({current_pnl_pct * 100:.1f}%)"

        # 条件2: 目标止盈
        elif current_pnl_pct >= profit_target:
            exit_reason = f"止盈 ({current_pnl_pct * 100:.1f}%)"

        # 条件3: 移动止损 (盈利超过阈值后启动)
        elif current_pnl_pct >= 0.01:  # 盈利1%后启动移动止损
            new_stop = entry_price * (1 + current_pnl_pct - 0.005)  # 保留0.5%利润
            if new_stop > stop_loss_price:
                position['stop_loss'] = new_stop

        # 条件4: 时段结束平仓（特别是盘前盘后）
        current_session = self.get_current_session()
        if position['session'] != current_session:
            exit_reason = f"时段结束 ({position['session']} -> {current_session})"

        # 执行出场
        if exit_reason:
            self.place_sell_order(symbol, exit_reason)

    def place_sell_order(self, symbol, reason):
        """下卖出订单"""
        try:
            position = self.positions[symbol]
            contract = position['contract']
            quantity = position['quantity']

            current_price = self.get_current_price(symbol)
            if current_price <= 0:
                current_price = position['entry_price']  # 使用入场价作为保底

            # 使用市价单确保成交
            order = MarketOrder('SELL', quantity)
            order.transmit = True

            trade = self.ib.placeOrder(contract, order)

            # 等待成交
            for i in range(10):
                if trade.orderStatus.status in ['Filled', 'Cancelled', 'ApiCancelled']:
                    break
                self.ib.sleep(1)

            if trade.orderStatus.status == 'Filled':
                fill_price = float(trade.orderStatus.avgFillPrice)
                entry_price = position['entry_price']
                pnl = (fill_price - entry_price) * quantity
                pnl_pct = (fill_price - entry_price) / entry_price * 100

                # 记录交易历史
                trade_record = {
                    'symbol': symbol,
                    'entry_price': entry_price,
                    'exit_price': fill_price,
                    'quantity': quantity,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'entry_time': position['entry_time'],
                    'exit_time': self.get_current_ny_time(),
                    'reason': reason,
                    'session': position['session']
                }
                self.trade_history.append(trade_record)

                logger.info(f"平仓 {symbol} | 原因: {reason} | "
                            f"入场: {entry_price:.2f} | 出场: {fill_price:.2f} | "
                            f"盈亏: ${pnl:.2f} ({pnl_pct:.2f}%)")

                # 移除持仓
                del self.positions[symbol]

        except Exception as e:
            logger.error(f"平仓失败 {symbol}: {e}")

    def print_status(self):
        """打印当前状态"""
        current_ny_time = self.get_current_ny_time()
        current_session = self.get_current_session()

        status_msg = f"\n=== 策略状态 ===\n"
        status_msg += f"纽约时间: {current_ny_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        status_msg += f"交易时段: {current_session}\n"
        status_msg += f"当前持仓: {len(self.positions)}/{self.max_positions}\n"

        if self.positions:
            status_msg += "持仓详情:\n"
            total_pnl = 0
            for symbol, position in self.positions.items():
                current_price = self.get_current_price(symbol)
                if current_price > 0:
                    pnl = (current_price - position['entry_price']) * position['quantity']
                    pnl_pct = (current_price - position['entry_price']) / position['entry_price'] * 100
                    total_pnl += pnl
                    status_msg += f"  {symbol}: {position['quantity']}股, 成本: {position['entry_price']:.2f}, 现价: {current_price:.2f}, 盈亏: ${pnl:.2f} ({pnl_pct:.2f}%)\n"

        if self.trade_history:
            today_trades = [t for t in self.trade_history
                            if t['exit_time'].date() == current_ny_time.date()]
            if today_trades:
                today_pnl = sum(t['pnl'] for t in today_trades)
                status_msg += f"今日交易: {len(today_trades)}笔, 总盈亏: ${today_pnl:.2f}\n"

        logger.info(status_msg)

    def run_strategy(self):
        """运行主策略"""
        logger.info("启动全时段交易策略...")
        self.setup_contracts()

        status_counter = 0

        try:
            while True:
                current_session = self.get_current_session()

                if not self.is_trading_hours():
                    if self.positions:
                        logger.info("非交易时间，平仓所有头寸")
                        for symbol in list(self.positions.keys()):
                            self.place_sell_order(symbol, "非交易时间平仓")
                    logger.info(f"市场关闭，当前时段: {current_session}，等待...")
                    time.sleep(60)
                    continue

                # 每30秒打印一次状态
                status_counter += 1
                if status_counter >= 3:  # 30秒 * 3 = 90秒
                    self.print_status()
                    status_counter = 0

                # 检查现有持仓的出场条件
                for symbol in list(self.positions.keys()):
                    self.check_exit_conditions(symbol)

                # 寻找新交易机会
                if len(self.positions) < self.max_positions:
                    for symbol in self.watchlist:
                        if symbol not in self.positions:
                            has_signal, entry_price, stop_loss_price = self.generate_trading_signals(symbol)

                            if has_signal:
                                logger.info(f"发现交易信号: {symbol} | 建议入场: {entry_price:.2f}")

                                quantity = self.calculate_position_size(entry_price, stop_loss_price)

                                if quantity > 0:
                                    success = self.place_buy_order(symbol, quantity, entry_price)
                                    if success:
                                        time.sleep(2)  # 等待订单处理
                                break  # 一次只建立一个新头寸

                # 等待一段时间再扫描
                time.sleep(10)

        except KeyboardInterrupt:
            logger.info("策略被用户中断")
        except Exception as e:
            logger.error(f"策略运行出错: {e}")
        finally:
            # 平仓所有头寸
            if self.positions:
                logger.info("平仓所有头寸...")
                for symbol in list(self.positions.keys()):
                    self.place_sell_order(symbol, "策略结束")

            # 打印最终统计
            if self.trade_history:
                total_pnl = sum(t['pnl'] for t in self.trade_history)
                win_trades = [t for t in self.trade_history if t['pnl'] > 0]
                win_rate = len(win_trades) / len(self.trade_history) * 100 if self.trade_history else 0

                logger.info(f"\n=== 最终统计 ===\n"
                            f"总交易次数: {len(self.trade_history)}\n"
                            f"胜率: {win_rate:.1f}%\n"
                            f"总盈亏: ${total_pnl:.2f}\n"
                            f"最终账户: ${self.account_value + total_pnl:.2f}")

            logger.info("策略停止")


# 主程序
if __name__ == "__main__":
    try:
        # 连接盈透
        ib = IB()
        ib.connect('127.0.0.1', 7496, clientId=1)
        logger.info("连接盈透TWS成功")

        # 打印账户信息
        account = ib.managedAccounts()[0]
        logger.info(f"交易账户: {account}")

        # 创建并运行策略
        strategy = AllDayTradingStrategy(ib)
        strategy.run_strategy()

    except Exception as e:
        logger.error(f"程序启动失败: {e}")
    finally:
        ib.disconnect()
        logger.info("断开连接")