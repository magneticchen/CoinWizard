#!/usr/bin/python3

import plotly.graph_objects as go
import pytz
eastern = pytz.timezone('US/Eastern')
utc = pytz.utc

from datetime import datetime
from coin_wizard.historical_pair_data import plot_historical_pair_data
# import state manager

class TradingAgent(object):
    def __init__(self, agent_directory):
        print(agent_directory)

    def _order_canceled_listener(self, order, reason):
        print('An order canceled.')

    def _order_filled_listener(self, order, trade):
        print(trade.getOpenPrice())
        print('An order filled.')

    def _trade_closed_listener(self, trade, realized_pl, close_price, spread, timestamp):
        print(trade.getOpenPrice())
        print(close_price)
        # print(datetime.now().timestamp()-timestamp.timestamp())

    def _run_loop(self, BrokerAPI):
        pass
        # print(BrokerAPI.getAccount().getUnrealizedPL())
        # print(123)


    def run(self, BrokerAPI):
        account = BrokerAPI.getAccount()
        orders = account.getOrders()
        trades = account.getTrades()
        print(account.getBalance())
        print(account.getUnrealizedPL())
        print(orders, trades)
        for order in orders:
            print(order.getInstrumentName(), order.getOrderSettings(), order.getTradeSettings())
            order.onCanceled(self._order_canceled_listener)
            order.onFilled(self._order_filled_listener)
            order.cancel()

        for trade in trades:
            print(trade.getInstrumentName(), trade.getTradeSettings())
            trade.onClosed(self._trade_closed_listener)
            trade.close()

        orders = account.getOrders()
        trades = account.getTrades()

        print(orders, trades)

        order = BrokerAPI.order('EUR_USD', {"type": "stop", "price": 2, "bound": 2.1}, {"units": 1, "take_profit": 2, "stop_lost": 0.5, "trailing_stop_distance": 0.001})
        order.onCanceled(self._order_canceled_listener)
        order.onFilled(self._order_filled_listener)
        print(order.order_id)

        order = BrokerAPI.order('EUR_USD', {"type": "market"}, {"units": 1, "take_profit": 2, "stop_lost": 0.5, "trailing_stop_distance": 0.1})
        order.onCanceled(self._order_canceled_listener)
        order.onFilled(self._order_filled_listener)
        print(order.order_id)

        # order = BrokerAPI.order('EUR_USD', {"type": "market"}, {"units": -2})
        # print(order.order_id)
        print(order.getOrderSettings())
        print(order.getTradeSettings())

        BrokerAPI.onLoop(self._run_loop)

    def stop_running(self, BrokerAPI):
        print('Agent stopped.')


    def train(self, BrokerAPI):
        plot_historical_pair_data('eurusd', eastern.localize(datetime(2021, 1, 8, 0, 0)), eastern.localize(datetime(2021, 1, 11, 23, 59)), 'US/Eastern')

    def stop_training(self, BrokerAPI):
        pass


    def test(self, BacktestBrokerAPI):
        self.run(BacktestBrokerAPI)

    def stop_testing(self, BacktestBrokerAPI):
        self.stop_running(BacktestBrokerAPI)
