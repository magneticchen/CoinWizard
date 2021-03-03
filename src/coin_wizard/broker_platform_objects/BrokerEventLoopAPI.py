#!/usr/bin/python3

import time
from datetime import datetime

def dummp_func(BrokerAPI):
    pass

class BrokerEventLoopAPI(object):
    def __init__(self, before_loop, after_loop, broker_settings, loop_interval_ms= 150):
        self.before_loop = before_loop
        self.after_loop = after_loop
        self.latest_loop_datetime = None
        self.loop_listener = dummp_func
        self.every_15_second_listener = dummp_func
        self.latest_every_15_second_loop_datetime = None
        self.loop_interval_ms = loop_interval_ms
        self.stopped = True

    def order(self, instrument_name, order_settings, trade_settings):
        pass

    def getInstrument(self, instrument_name):
        pass

    def getAccount(self):
        return self.account

    def onLoop(self, loop_listener):
        self.loop_listener = loop_listener

    def onEvery15Second(self, every_15_second_listener):
        self.every_15_second_listener = every_15_second_listener

    def _stop(self):
        if self.stopped:
            return
        self.stopped = True

    def _loop(self):
        pass

    def _loop_wrapper(self):
        # start_loop_timeStamp = datetime.now().timestamp()
        self.before_loop()
        self._loop()
        if 1000*(datetime.now().timestamp() - self.latest_every_15_second_loop_datetime.timestamp()) > 15000:
            self.every_15_second_listener(self)
            self.latest_every_15_second_loop_datetime = datetime.now()
        self.loop_listener(self)
        self.after_loop()
        
        end_loop_timestamp = datetime.now().timestamp()
        time_passed_ms = (end_loop_timestamp - self.latest_loop_datetime.timestamp())*1000

        every_15_second_loop_remain_ms = 15000 - (end_loop_timestamp - self.latest_every_15_second_loop_datetime.timestamp())*1000
        # print('every_15_second_loop_remain_ms', every_15_second_loop_remain_ms)
        if every_15_second_loop_remain_ms < (self.loop_interval_ms - time_passed_ms):
            if every_15_second_loop_remain_ms > 0:
                time.sleep(0.001*(every_15_second_loop_remain_ms))
            self.every_15_second_listener(self)
            self.latest_every_15_second_loop_datetime = datetime.now()
            end_loop_timestamp = datetime.now().timestamp()

        time_passed_ms = (end_loop_timestamp - self.latest_loop_datetime.timestamp())*1000
        # print('time_passed_ms', time_passed_ms, self.loop_interval_ms)
        if(time_passed_ms < self.loop_interval_ms):
            # print(0.001*self.loop_interval_ms - time_passed_ms)
            time.sleep(0.001*(self.loop_interval_ms - time_passed_ms))

    def _run_loop(self):
        self.stopped = False
        self.latest_loop_datetime = datetime.now()
        self.latest_every_15_second_loop_datetime = datetime.now()
        while True:
            if self.stopped:
                return
            self._loop_wrapper()
            self.latest_loop_datetime = datetime.now()
