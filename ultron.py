# encoding: utf-8

import time

from ironman import Ironman
from vision import Vision

sprint = lambda string: Ironman.sprint(speaker="奥创", string=string)
to_datetime = Ironman.to_datetime
now_datetime = Ironman.now_datetime
thread = Ironman.thread

# todo: 优化打印的注释内容


class Ultron(object):
    def __init__(self,
                 symbol1,
                 symbol2,
                 contract1,
                 contract2,
                 port1=6001,
                 port2=6002,
                 history_period=400,
                 history_longer=100,
                 std_bands=0.5,
                 ):

        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.contract1 = contract1
        self.contract2 = contract2

        self.PORT1 = port1
        self.PORT2 = port2
        self.HISTORY_PERIOD = history_period
        self.HISTORY_LONGER = history_longer
        self.STD_BANDS = std_bands

        # to: 主要的条件变量
        self.unit_band_up = None
        self.unit_band_down = None
        self.condition_evaluate_timestamp = None

        # 记录vision的历史数据是否加载完毕
        # 如果加载完毕，结果应该为两个True
        self.vision_history_collect_complete = []

        self.ultron_started = False
        self.ultron_is_working = False
        self.ultron_already = False

        # 为幻视提供改写奥创数据的接口
        self.vision_ticker_dict = {
            1: None,
            2: None
        }

        self.vision_tickers_dict = {
            1: None,
            2: None
        }

        # 为奥创添加一对vision
        self.vision1 = Vision(ultron=self,
                              vision_num=1,
                              port=port1,
                              history_period=history_period,
                              history_longer=history_longer)
        self.vision2 = Vision(ultron=self,
                              vision_num=2,
                              port=port2,
                              history_period=history_period,
                              history_longer=history_longer)

    @property
    def ticker1(self):
        return self.vision_ticker_dict[1]

    @property
    def ticker2(self):
        return self.vision_ticker_dict[2]

    @property
    def tickers1(self):
        return self.vision_tickers_dict[1]

    @property
    def tickers2(self):
        return self.vision_tickers_dict[2]

    @property
    def unit_cost(self):
        return self.ticker1["a1"] * 1.0003 - self.ticker2["b1"]

    @property
    def unit_earning(self):
        return self.ticker1["b1"] - self.ticker2["a1"] * 1.0003

    # to: 主函数
    def start(self):
        self.vision1.start()
        self.vision2.start()
        self.__ultron_start()

        while not self.ultron_is_working:
            sprint("奥创的工作状态：" + str(self.ultron_is_working))
            sprint("奥创启动中，请再等待5秒钟\n")
            time.sleep(5)

        while self.unit_band_up is None or self.unit_band_down is None:
            sprint("奥创还在准备数据，请稍等五秒钟。\n")
            time.sleep(5)

        sprint("\n奥创已经彻底启动，可以对接鹰眼了。\n")
        # while True:
        #     time.sleep(0.5)
        #     a = self.unit_band_up - self.unit_earning
        #     b = self.unit_cost - self.unit_band_down
        #     sprint(str(a) + "  " + str(b))
        #     if a < 0 or b < 0:
        #         sprint("#################################A Chance################################\n")

    # to: 主函数的内部函数
    def __ultron_start(self):
        self.ultron_started = True

        def ultron_start_unthread():

            if len(self.vision_history_collect_complete) == 2:

                self.__has_vision_prepared_tickers()

                while True:
                    time.sleep(1)
                    self.__evaluate_conditions()

            else:
                time.sleep(self.HISTORY_PERIOD + self.HISTORY_LONGER + 10)

                self.__has_vision_prepared_history_data()

                # to: 确保肯定不会再读到这里来了。
                self.vision_history_collect_complete = [True, True]

                ultron_start_unthread()

        thread(ultron_start_unthread)

    # to: 主要工作函数 更新判断条件：unit_band_up, unit_band_down
    def __evaluate_conditions(self):

        tickers1_temp = self.tickers1
        tickers2_temp = self.tickers2

        # 单位成本，即S2
        unit_costs = tickers1_temp["a1"] * 1.0003 - tickers2_temp["b1"]

        # 单位收益，即S1(S1 < S2恒成立)
        unit_earnings = tickers1_temp["b1"] - tickers2_temp["a1"] * 1.0003

        # 盘口中点
        unit_mids = (unit_costs + unit_earnings) / 2
        unit_mids = unit_mids.dropna()

        # 盘口中点的EWMA
        unit_means = unit_mids.ewm(span=self.HISTORY_PERIOD,
                                   min_periods=self.HISTORY_PERIOD).mean()

        # 盘口中点的StD
        unit_stds = unit_mids.rolling(str(self.HISTORY_PERIOD) + "s",
                                      min_periods=self.HISTORY_PERIOD).std()

        unit_band_up_temp = unit_means[-1] + unit_stds[-1] * self.STD_BANDS
        unit_band_down_temp = unit_means[-1] - unit_stds[-1] * self.STD_BANDS

        # to: 如果两个值中的一个没计算出来，那么两秒后重算一次
        if unit_band_up_temp is None or unit_band_down_temp is None:
            sprint("奥创没有计算出这次的band-up和band-down")
            sprint("检查一下是不是History-Longer参数需要调大。\n")
        else:
            self.unit_band_up = unit_band_up_temp
            self.unit_band_down = unit_band_down_temp
            self.condition_evaluate_timestamp = now_datetime()

            if not self.ultron_already:
                self.ultron_already = True
                sprint("一切准备就绪。\nLet the trade begin.\n\n")

    # to: 一些重要的判断
    def __has_vision_prepared_tickers(self):
        while self.tickers1 is None or self.tickers2 is None:
            sprint("幻视还没有把Tickers整理好，请再等待5秒钟。\n")
            time.sleep(5)
        self.ultron_is_working = True
        sprint("幻视整理好了Tickers。\n")
        sprint("奥创启动。\n")

    def __has_vision_prepared_history_data(self):
        while len(self.vision_history_collect_complete) != 2:
            sprint("幻视还没有把History整理好，请再等待5秒钟。\n")
            time.sleep(5)
        sprint("幻视整理好了History。\n")


