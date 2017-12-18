##
import requests as r
import json
import time
import pandas as pd


##
class Bittrex(object):
    def __init__(self):
        pass

    @staticmethod
    def _publicUrl(command):
        return "https://bittrex.com/api/v1.1/public/" + command

    @staticmethod
    def _publicRequest(command, parameters=None):
        request = r.get(Bittrex._publicUrl(command)) \
            if parameters is None \
            else \
            r.get(Bittrex._publicUrl(command),
                  params=parameters)
        return json.loads(request.text)

    @staticmethod
    def get_markets():
        return Bittrex._publicRequest("getmarkets")["result"]

    @staticmethod
    def get_currencyInfo():
        return Bittrex._publicRequest("getcurrencies")["result"]

    @staticmethod
    def get_ticker(market):
        """

        :param market: required	a string literal for the market (ex: BTC-LTC)
        :return:
        """
        return Bittrex._publicRequest("getticker",
                              {"market": market})["result"]

    @staticmethod
    def get_stats():
        return Bittrex._publicRequest("getmarketsummaries")["result"]

    @staticmethod
    def get_marketInfo(market):
        """

        :param market:	required a string literal for the market (ex: BTC-LTC)
        :return:
        """
        return Bittrex._publicRequest("getmarketsummary",
                              {"market": market})["result"]

    @staticmethod
    def get_orderbook(market, type="both"):
        """

        :param market: required	a string literal for the market (ex: BTC-LTC)
        :param type:   required	buy, sell or both to identify the type of orderbook to return.
        :return:
        """
        return Bittrex._publicRequest("getorderbook",
                              {"market": market,
                               "type": type})["result"]

    @staticmethod
    def get_marketHistory(market):
        return Bittrex._publicRequest("getmarkethistory",
                              {"market": market})["result"]


