# encoding: utf-8

from config import Config
from ironman import Ironman
import pandas as pd
import websocket
from broker import Broker
import time

sprint = lambda string: Ironman.sprint(speaker="菲利普", string=string)
to_datetime = Ironman.to_datetime
now_datetime = Ironman.now_datetime
thread = Ironman.thread
sign = Ironman.sign

class Phil(object):
    def __init__(self, symbol1, symbol2, contract1, contract2):

        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.contract1 = contract1
        self.contract2 = contract2

        sprint("菲利普准备行动。")

        self.broker = Broker()
        sprint("菲利普呼叫了交易商。")

        self.long_on_match1 = lambda amount: self.broker.long_on_match(symbol1, contract1, amount)
        self.long_on_match2 = lambda amount: self.broker.long_on_match(symbol2, contract2, amount)

        self.short_on_match1 = lambda amount: self.broker.short_on_match(symbol1, contract1, amount)
        self.short_on_match2 = lambda amount: self.broker.short_on_match(symbol2, contract2, amount)

        self.close_long_on_match1 = lambda amount: self.broker.close_long_on_match(symbol1, contract1, amount)
        self.close_long_on_match2 = lambda amount: self.broker.close_long_on_match(symbol2, contract2, amount)

        self.close_short_on_match1 = lambda amount: self.broker.close_short_on_match(symbol1, contract1, amount)
        self.close_short_on_match2 = lambda amount: self.broker.close_short_on_match(symbol2, contract2, amount)

        self.long_position_info1 = self.broker.long_position_info(symbol1, contract1)
        self.long_position_info2 = self.broker.long_position_info(symbol2, contract2)

        self.short_position_info1 = self.broker.short_position_info(symbol1, contract1)
        self.short_position_info2 = self.broker.short_position_info(symbol2, contract2)

        sprint("菲利普准备完毕。")

        self.__refresh_position_info()
        sprint("菲利普开始刷新仓位信息。")

    def __refresh_position_info(self):

        def unthread_position_info():
            total_error = 0
            while True:
                try:
                    time.sleep(2)
                    self.long_position_info1 = self.broker.long_position_info(self.symbol1, self.contract1)
                    self.long_position_info2 = self.broker.long_position_info(self.symbol2, self.contract2)

                    time.sleep(2)
                    self.short_position_info1 = self.broker.short_position_info(self.symbol1, self.contract1)
                    self.short_position_info2 = self.broker.short_position_info(self.symbol2, self.contract2)
                except:
                    time.sleep(2)
        thread(unthread_position_info)

# ##
# phil = Phil("btc_usd", "btc_usd", "this_week", "next_week")
# ##
# phil.long_position_info1
#
#
