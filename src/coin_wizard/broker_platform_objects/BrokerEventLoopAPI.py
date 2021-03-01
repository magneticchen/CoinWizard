#!/usr/bin/python3

import time
from datetime import datetime

def dummp_func():
    pass

class BrokerEventLoopAPI(object):
    def __init__(self, before_loop, after_loop, broker_settings, loop_interval_ms= 50):
        self.before_loop = before_loop
        self.after_loop = after_loop
        self.latest_loop_datetime = None
        self.loop_listener = dummp_func
        self.loop_interval_ms = loop_interval_ms
        self.stopped = True

    def order(self, order_settings, trade_settings):
        pass

    def getInstrument(self, instrument_name):
        pass

    def getAccount(self):
        return self.account

    def onLoop(self, loop_listener):
        self.loop_listener = loop_listener

    def _stop(self):
        if self.stopped:
            return
        self.stopped = True

    def _loop(self):
        pass

    def _loop_wrapper(self):
        start_loop_timeStamp = datetime.now().timestamp()
        self.before_loop()
        self._loop()
        self.loop_listener()
        self.after_loop()
        end_loop_timeStamp = datetime.now().timestamp()
        time_passed_ms = end_loop_timeStamp - start_loop_timeStamp
        if(time_passed_ms < self.loop_interval_ms):
            time.sleep(0.001*self.loop_interval_ms - time_passed_ms)

    def _run_loop(self):
        self.stopped = False
        while True:
            if self.stopped:
                return
            self._loop_wrapper()