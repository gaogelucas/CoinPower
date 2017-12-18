# encoding: utf-8


##
import requests as r
import json
import time
##
#&end=1506412800000
url = "https://api.bitfinex.com/v2/candles/trade:1D:tEOSUSD/hist?limit=1000"
request = r.get(url)
result = request.json()
##
class Bitfinex_v2(object):
    def __init__(self,
                 api_key,
                 api_sn):
        self.api_key = api_key
        self.api_sn = api_sn

    @staticmethod
    def _url(endpoint):
        return "https://api.bitfinex.com/v2/" + endpoint

class Bitfinex(object):
    def __init__(self,
                 api_key,
                 api_sn):
        self.api_key = api_key
        self.api_sn = api_sn

    @staticmethod
    def _url(endpoint):
        return "https://api.bitfinex.com/v1/" + endpoint

    @staticmethod
    def _timestamp(dateStr, format="%Y-%m-%d %H:%M:%S"):
        return time.mktime(time.strptime(dateStr, format))

    @staticmethod
    def get_symbols():
        request = r.get(Bitfinex._url("symbols"))
        return json.loads(request.text)

    @staticmethod
    def get_symbolsDetail():
        """

        :return:
            pair	            [string]	The pair code
            price_precision	    [integer]	Maximum number of significant digits for price in this pair
            initial_margin	    [decimal]	Initial margin required to open a position in this pair
            minimum_margin	    [decimal]	Minimal margin to maintain (in %)
            maximum_order_size	[decimal]	Maximum order size of the pair
            expiration	        [string]	Expiration date for limited contracts/pairs
        """
        request = r.get(Bitfinex._url("symbols_details"))
        return json.loads(request.text)

    @staticmethod
    def get_stats(symbol):
        """

        :param symbol:
        :return:
            period	    [integer]	Period covered in days
            volume	    [price]	    Volume
        """
        request = r.get(Bitfinex._url("stats/") + symbol.lower())
        return json.loads(request.text)

    @staticmethod
    def get_ticker(symbol):
        """

        :param symbol:
        :return:
            mid	        [price]	    (bid + ask) / 2
            bid	        [price]	    Innermost bid
            ask	        [price]	    Innermost ask
            last_price	[price]	    The price at which the last order executed
            low	        [price]	    Lowest trade price of the last 24 hours
            high	    [price]	    Highest trade price of the last 24 hours
            volume	    [price]	    Trading volume of the last 24 hours
            timestamp	[time]	    The timestamp at which this information was valid
        """
        request = r.get(Bitfinex._url("pubticker/") + symbol.lower())
        return json.loads(request.text)

    @staticmethod
    def get_orderbook(symbol, depth=10, group=1):
        """

        :param symbol:
        :param depth: Limit the number of bids and asks returned.
        :param group:   If 1, orders are grouped by price in the orderbook.
                        If 0, orders are not grouped and sorted individually.
        :return:
            bids	    [array]
            price	    [price]
            amount	    [decimal]
            timestamp	[time]
            asks	    [array]
            price	    [price]
            amount	    [decimal]
            timestamp	[time]
        """
        request = r.get(Bitfinex._url("book/") + symbol.lower(),
                        params={"limit_bids": depth,
                                "limit_asks": depth,
                                "group": group})
        return json.loads(request.text)

    @staticmethod
    def get_trades(symbol, timestamp=0, limit_trades=50):
        """

        :param symbol:
        :param timestamp:       ["%Y-%m-%d %H:%M:%S"]   Only show trades at or after this timestamp.
        :param limit_trades:    [int]                   Limit the number of trades returned. Must be >= 1.
        :return:
            tid	        [integer]
            timestamp	[time]
            price	    [price]
            amount	    [decimal]
            exchange	[string]	"bitfinex"
            type	    [string]	“sell” or “buy” (can be “” if undetermined)
        """
        request = r.get(Bitfinex._url("trades/") + symbol.lower(),
                        params={"timestamp": Bitfinex._timestamp(timestamp),
                                "limit_trades": limit_trades} if timestamp != 0 else {"limit_trades": limit_trades})
        return json.loads(request.text)

    @staticmethod
    def get_fundingbook(currency, limit_bids=50, limit_asks=50):
        """

        :param currency:
        :param limit_bids: Limit the number of funding bids returned.
        :param limit_asks: Limit the number of funding asks returned.
        :return:
            bids	    [array of funding bids]
            rate	    [rate in % per 365 days]
            amount	    [decimal]
            period	    [days]	                    Minimum period for the margin funding contract
            timestamp	[time]
            frr	        [yes/no]	                “Yes”: offer is at Flash Return Rate, “No” :the offer at fixed rate
            asks	    [array of funding offers]
            rate	    [rate in % per 365 days]
            amount	    [decimal]
            period	    [days]	                    Maximum period for the funding contract
            timestamp	[time]
            frr	        [yes/no]	                “Yes”: offer is at Flash Return Rate, “No” :the offer at fixed rate
        """
        request = r.get(Bitfinex._url("lendbook/") + currency.lower(),
                        params={"limit_bids": limit_bids,
                                "limit_asks": limit_asks})
        return json.loads(request.text)

    @staticmethod
    def get_lends(currency, timestamp=0, limit_lends=50):
        """

        :param currency:
        :param timestamp:       ["%Y-%m-%d %H:%M:%S"]   Only show data at or after this timestamp
        :param limit_lends:     [int]	50	            Limit the amount of funding data returned. Must be >= 1
        :return:
            rate	    [decimal, % by 365 days]	Average rate of total funding received at fixed rates annualized
            amount_lent	[decimal]	                Total amount of open margin funding in the given currency
            amount_used	[decimal]	                Total amount of open margin funding used in a margin position
            timestamp	[time]
        """
        request = r.get(Bitfinex._url("lends/" + currency.lower()),
                        params={"timestamp": Bitfinex._timestamp(timestamp),
                                "limit_lends": limit_lends} if timestamp != 0 else {"limit_lends": limit_lends})
        return json.loads(request.text)
