# encoding: utf-8

from zeroless import Client
import pandas as pd
import numpy as np
from config import Config
import time
from ironman import Ironman


class Vision(object):
    def __init__(self,
                 ultron=None,
                 vision_num=None,
                 port=6001,
                 history_period=800,
                 history_longer=5):

        config = Config(port=port)

        self.THERE_IS_AN_ULTRON = False if ultron is None else True

        # to: 如果存在ultron，则挂载ultron以及Ultron的各种接口
        if ultron is not None:
            self.ultron = ultron
            self.vision_ticker_dict = ultron.vision_ticker_dict
            self.vision_tickers_dict = ultron.vision_tickers_dict
            self.vision_num = vision_num

        #
        self.HISTORY_PERIOD = history_period
        self.HISTORY_LONGER = history_longer
        self.EVALUATE_PADAS_LAG = config.evaluate_pandas_tickers_lag
        self.START_TIME = None  # start_listen任务的开始时间，Pandas.datetime
        self.START_TIME_ABSOLUTE = None  # start_listen任务的开始时间，float

        # 连接数据流，建立监听器
        self.PORT = port
        self.watcher = self.__build_watcher()

        #
        self.ticker = None
        self.tickers = None

        #
        self.__history_collect_complete = False
        self.__ticker_list_temp = []

    # to: 主函数
    # 监听并处理数据
    def start(self):
        def vision_watcher_unthread():
            self.START_TIME_ABSOLUTE = time.time()
            self.START_TIME = pd.to_datetime(time.time())

            for ticker_str in self.watcher.sub():
                ticker_dict = self.__build_ticker_dict(ticker_str)

                # 刷新self.ticker
                self.__evaluate_ticker(ticker_dict)

                # 向self.__ticker_list_temp添加ticker数据
                self.__ticker_list_temp.append(ticker_dict)

                # to: 运行数据处理的主要逻辑
                # 更新历史数据
                # 更新现在的tickers等
                self.__perform_data_logic()
        Ironman.thread(target=vision_watcher_unthread)

    # to: 主要的逻辑函数
    def __perform_data_logic(self):
        if self.__history_collect_complete:  # 如果历史数据收集完毕
            # 根据预定的self.EVALUATE_PADAS_LAG刷新Pandas
            if len(self.__ticker_list_temp) > self.EVALUATE_PADAS_LAG:
                # evaluate pandas and cut it to a proper size
                self.__evaluate_tickers()
                # -> 更新tickers
                # -> 清空self.__ticker_list_temp

        else:  # 如果历史数据没有收集完毕，那么继续收集
            # 如果从开始到现在，时间已经粗略的超过了历史数据的要求
            if time.time() - self.START_TIME_ABSOLUTE >= self.HISTORY_PERIOD + self.HISTORY_PERIOD:
                self.__collect_history_data()
                # -> self.__history_collect_complete = True
                # -> self.tickers 生成
                # -> self.ticker_list_temp 被清空重置
                # -> 告知ultron我已经完成

    # to: 工具函数 建立Listener监听器
    def __build_watcher(self):
        client = Client()
        client.connect_local(port=self.PORT)
        return client

    # to: 工具函数 处理ticker数据
    @staticmethod
    def __build_ticker_dict(ticker_str):
        ticker_dict = dict([item.split(":", 1)
                            for item in ticker_str[1:-1].replace("\"", "").split(",")])

        for key in ticker_dict:
            try:
                ticker_dict[key] = float(ticker_dict[key])
            except:
                ticker_dict[key] = ticker_dict[key]

        # to: 判断这次更新的是order还是trade，并确定使用哪个时间戳
        if ticker_dict["update_type"] == 1:
            ticker_dict["time"] = ticker_dict["order_date_time"]
        else:
            ticker_dict["time"] = ticker_dict["trades_date_time"]

        return ticker_dict

    def __build_tickers(self):

        new_tickers = pd.DataFrame(self.__ticker_list_temp)
        new_tickers.index = pd.to_datetime(new_tickers["time"])
        new_tickers = new_tickers.resample("1S").mean().ffill()
        return new_tickers

    def __clear_ticker_list_temp(self):
        self.__ticker_list_temp = []

    def __collect_history_data(self):

        # 如果超过了历史数据时间要求：
        if pd.to_datetime(self.ticker["order_date_time"]) - self.START_TIME > \
                pd.Timedelta(str(self.HISTORY_PERIOD + self.HISTORY_LONGER) + " seconds"):
            self.__history_collect_complete = True
            self.tickers = self.__build_tickers()

            # to: 如果挂载了utron，则向ultron传递已经完成的信号
            if self.THERE_IS_AN_ULTRON is not None:
                self.ultron.vision_history_collect_complete.append(True)

            self.__clear_ticker_list_temp()

            # 如果没有超过历史数据时间要求，那么不予理会。

    def __evaluate_ticker(self, ticker_dict):
        self.ticker = ticker_dict

        # to: 向奥创暴露数据
        if self.THERE_IS_AN_ULTRON:
            self.vision_ticker_dict[self.vision_num] = ticker_dict

    def __evaluate_tickers(self):
        new_tickers = self.__build_tickers()

        self.tickers = pd.concat([self.tickers, new_tickers], axis=0)

        # to: 在concat之后，对tickers还应该进行一次重采样
        self.tickers = self.tickers.resample("1S").mean().ffill()

        # to: 在重采样后，还要把pandas裁剪到方便计算的宽度
        self.tickers = self.tickers[-100 - self.HISTORY_LONGER - self.HISTORY_PERIOD:]

        # to: 向奥创暴露tickers数据
        if self.THERE_IS_AN_ULTRON:
            self.vision_tickers_dict[self.vision_num] = self.tickers

        self.__clear_ticker_list_temp()

