##
import requests as r
import json
import time
import pandas as pd


##
class Cryptopia(object):
    def __init__(self):
        pass

    @staticmethod
    def _publicUrl(command):
        return "https://www.cryptopia.co.nz/api/" + command

    @staticmethod
    def _publicRequest(command, parameters=None):
        if parameters is None:
            parameters = []
        for parameter in parameters:
            command += ("/" + str(parameter))
        request = r.get(Cryptopia._publicUrl(command))
        return json.loads(request.text)

    @staticmethod
    def get_currencyInfo():
        return Cryptopia._publicRequest("getcurrencies")["Data"]

    @staticmethod
    def get_tradePairs():
        return Cryptopia._publicRequest("getTradePairs")["Data"]

    @staticmethod
    def get_markets(baseMarket=None):
        if baseMarket is None:
            return Cryptopia._publicRequest("getmarkets")["Data"]
        else:
            return Cryptopia._publicRequest("getmarkets",
                                           parameters=[baseMarket])["Data"]

    @staticmethod
    def get_marketHistory(market):
        return Cryptopia._publicRequest("getmarkethistory",
                                       parameters=[market])["Data"]

    @staticmethod
    def get_marketOrders(market, depth=10):
        return Cryptopia._publicRequest("getmarketorders",
                                       parameters=[market, depth])
