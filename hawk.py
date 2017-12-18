# encoding: utf-8

import time

from config import Config
from ironman import Ironman
from phil import Phil
from ultron import Ultron

sprint = lambda string: Ironman.sprint(speaker="鹰眼", string=string)
to_datetime = Ironman.to_datetime
now_datetime = Ironman.now_datetime
thread = Ironman.thread

config = Config()
api_key = config.api_key
secret_key = config.secret_key
ok_future_url = config.okfuture_api_url
##


class Hawk(object):
    def __init__(self, ultron):
        sprint("鹰眼准备启动。")

        self.ultron = ultron
        sprint("鹰眼对接了奥创。")

        self.symbol1 = ultron.symbol1
        self.symbol2 = ultron.symbol2
        self.contract1 = ultron.contract1
        self.contract2 = ultron.contract2

        sprint("鹰眼呼叫了菲利普。")
        self.phil = Phil(self.symbol1, self.symbol2, self.contract1, self.contract2)

        self.ticker1 = None
        self.ticker2 = None
        self.band_up = None
        self.band_down = None
        self.cost = None
        self.earning = None

        # s1是Earning，也就是卖出资产1，买入资产2的收入
        # s1上穿代表收益很大，也就是是时候这么做了
        self.earning_up = None

        # s2是Cost，也就是卖出资产2，买入资产1的成本
        # s2下穿代表成本很小，也就是是时候这么做了
        self.cost_down = None

        sprint("鹰眼准备完毕，鹰眼可以启动了。")

    def start(self):
        self.__ultron_start()
        sprint("奥创已经完全启动。\n")
        sprint("鹰眼上线。\n")

        self.__hawk_the_market()

    def __hawk_the_market(self):

        def unthread_hawk():
            sprint("鹰眼已经启动。\n")
            sprint("#### enjoy trading ####\n")

            while True:
                time.sleep(0.05)
                self.ticker1 = self.ultron.ticker1
                self.ticker2 = self.ultron.ticker2
                self.band_up = self.ultron.unit_band_up
                self.band_down = self.ultron.unit_band_down

                self.cost = self.ticker1["a1"] * 1.0003 - self.ticker2["b1"]
                self.earning = self.ticker1["b1"] - self.ticker2["a1"] * 1.0003

                # s1是Earning，也就是卖出资产1，买入资产2的收入
                # s1上穿代表收益很大，也就是是时候这么做了
                self.earning_up = self.earning - self.band_up

                # s2是Cost，也就是卖出资产2，买入资产1的成本
                # s2下穿代表成本很小，也就是是时候这么做了
                self.cost_down = self.band_down - self.cost
                sprint("距离S1上穿 " + str(-self.earning_up) + " 距离S2下穿 " + str(-self.cost_down))
                if self.earning_up > 0:
                    sprint("############ 触发交易信号：S1上穿 ############")
                    sprint("############ 做空：资产1 ####################")
                    sprint("############ 做多：资产2 ####################")

                    best_amount = min([self.ticker1["bq1"], self.ticker2["aq1"]])

                    self.__deal_earning_up(best_amount)

                elif self.cost_down > 0:
                    sprint("############ 触发交易信号：S2下穿 ############")
                    sprint("############ 做空：资产2 ####################")
                    sprint("############ 做多：资产1 ####################")

                    best_amount = min([self.ticker1["aq1"], self.ticker2["bq1"]])

                    self.__deal_cost_down(best_amount)

        thread(unthread_hawk)

    def __ultron_start(self):
        sprint("检查奥创是否启动。\n")
        self.__have_ultron_started()
        sprint("检查奥创是否准备完毕。\n")
        self.__have_ultron_prepared()

    def __have_ultron_started(self):
        if not self.ultron.ultron_started:
            sprint("奥创尚未启动，马上启动奥创。\n")
            self.ultron.start()
        time.sleep(3)
        if self.ultron.ultron_started:
            sprint("奥创已经启动，开始进行准备工作，请耐心等待。")
            return
        else:
            self.__have_ultron_started()

    def __have_ultron_prepared(self):
        if not self.ultron.ultron_already:
            expected_time = self.ultron.HISTORY_LONGER + self.ultron.HISTORY_PERIOD + 10

            sprint("奥创正在处理数据，预计需要 " +
                   str(expected_time) +
                   " 秒，请耐心等待。\n")
            while not self.ultron.ultron_already:
                time.sleep(10)
                expected_time -= 10

                if expected_time > 0:
                    sprint("奥创正在处理数据，预计需要 " +
                           str(expected_time) +
                           " 秒，请耐心等待。\n")

                else:
                    sprint("奥创的准备工作比预计要久 " +
                           str(-expected_time) +
                           " 秒，请耐心等待。\n")

        sprint("奥创已经准备好了，让您久等了。\n")

    def __deal_earning_up(self, best_amount):
        asset_long_position1 = self.phil.long_position_info1["amount"]

        if asset_long_position1 > 0:
            if asset_long_position1 > best_amount:
                self.phil.close_long_on_match1(best_amount)
                self.phil.close_short_on_match2(best_amount)
                sprint("#### 抓紧机会，平多资产1，平空资产2 ####")

            else:
                self.phil.close_long_on_match1(asset_long_position1)
                self.phil.close_short_on_match2(asset_long_position1)
                self.phil.short_on_match1(best_amount - asset_long_position1)
                self.phil.long_on_match2(best_amount - asset_long_position1)
                sprint("#### 抓紧机会，平多资产1，平空资产2 ####")
                sprint("#### 抓紧机会，买空资产1，买多资产2 ####")

        else:
            self.phil.short_on_match1(best_amount)
            self.phil.long_on_match2(best_amount)
            sprint("#### 抓紧机会，买空资产1，买多资产2 ####")

    def __deal_cost_down(self, best_amount):
        asset_short_position1 = self.phil.short_position_info1["amount"]

        if asset_short_position1 > 0:
            if asset_short_position1 > best_amount:
                self.phil.close_short_on_match1(best_amount)
                self.phil.close_long_on_match2(best_amount)
                sprint("#### 抓紧机会，平多资产2，平空资产1 ####")

            else:
                self.phil.close_short_on_match1(asset_short_position1)
                self.phil.close_long_on_match2(asset_short_position1)
                self.phil.long_on_match1(best_amount - asset_short_position1)
                self.phil.short_on_match2(best_amount - asset_short_position1)
                sprint("#### 抓紧机会，平多资产2，平空资产1 ####")
                sprint("#### 抓紧机会，买空资产2，买多资产1 ####")

        else:
            self.phil.long_on_match1(best_amount)
            self.phil.short_on_match2(best_amount)
            sprint("#### 抓紧机会，买空资产2，买多资产1 ####")


