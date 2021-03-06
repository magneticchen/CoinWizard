#!/usr/bin/python3
#
# def dummp_func(a, b, c, d, e):
#     print('A trade close has been skipped. Since event not registered.')

class Trade(object):
    def __init__(self, trade_id, instrument_name, open_price, trade_settings, update_trade):
        self.trade_id = trade_id
        self.instrument_name = instrument_name
        self.open_price = open_price
        self.trade_settings = trade_settings
        self.price = open_price
        self.unrealized_pl = 0
        self.reduced_listener = None
        self.closed_listener = None
        self.closed = False
        self.update_trade = update_trade
        self.reduce_handler = None
        self.close_handler = None

    def close(self):
        if self.closed:
            raise Exception('Trade already closed.')
        return self.close_handler(self)

    def modify(self, trade_settings):
        if self.closed:
            raise Exception('Trade already closed.')
        return self.modify_handler(self, trade_settings)

    def reduce(self, units):
        if self.closed:
            raise Exception('Trade already closed.')
        return self.reduce_handler(self, units)

    def getInstrumentName(self):
        return self.instrument_name

    def getOpenPrice(self):
        return self.open_price

    def getTradeSettings(self):
        self.update_trade(self)
        return self.trade_settings

    def getUnrealizedPL(self):
        self.update_trade(self)
        return self.unrealized_pl

    def onReduced(self, reduced_listener):
        self.reduced_listener = reduced_listener

    def onClosed(self, closed_listener):
        self.closed_listener = closed_listener
