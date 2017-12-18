# encoding: utf-8

from OKCoin.OkcoinFutureAPI import OKCoinFuture

from config import Config
from ironman import Ironman

##
sprint = lambda string: Ironman.sprint(speaker="交易商", string=string)
to_datetime = Ironman.to_datetime
now_datetime = Ironman.now_datetime
thread = Ironman.thread
sign = Ironman.sign
get = Ironman.httpGet
post = Ironman.httpPost


class Broker(object):
    def __init__(self):
        sprint("交易商正在链接Restful API。")
        self.rest = OKCoinFuture(Config())
        self.API_URL = "https://www.okex.com/api/v1"
        self.TRADE_URL = "/api/v1/future_trade.do?"

        config = Config()

        self.API_KEY = config.api_key
        self.SECRET = config.secret_key

        sprint("交易商准备完毕。")
        sprint("可以开始交易了。")

    # ------------------------------------------------------------ #

    def long_position_info(self, symbol, contract_type):
        position_info = self.position_info(symbol, contract_type)
        if position_info["holding"]:
            holding = position_info["holding"][0]
            return {
                "amount": holding["buy_amount"],
                "available": holding["buy_available"]
            }
        else:
            return {
                "amount": 0,
                "available": 0
            }

    def short_position_info(self, symbol, contract_type):
        position_info = self.position_info(symbol, contract_type)
        if position_info["holding"]:
            holding = position_info["holding"][0]
            return {
                "amount": holding["sell_amount"],
                "available": holding["sell_available"]
            }
        else:
            return {
                "amount": 0,
                "available": 0
            }

    # ------------------------------------------------------------ #

    def account_info(self):
        return self.rest.future_userinfo()

    def position_info(self, symbol, contract_type):
        return self.rest.future_position(symbol, contract_type)

    def ticker(self, symbol, contract_type):
        return self.rest.future_ticker(symbol, contract_type)

    # ------------------------------------------------------------ #

    # to: 取消订单，需要提前记录订单号
    def cancel(self, symbol, contract, order_id):
        self.rest.future_cancel(symbol, contract, order_id)

    # ------------------------------------------------------------ #
    def trade(self, symbol, contract, amount, price, order_type, match_trade=False, lever_rate=10):
        params = self.__make_trade_parameters(symbol, contract, price, amount, order_type, match_trade, lever_rate)
        result = post(self.API_URL, self.TRADE_URL, params)
        if result["result"]:
            sprint("订单发出成功，订单ID为 " + str(result["order_id"]))
        else:
            sprint("订单发出失败，检查是否网络有问题，或者订单字典有误。")
        return result

    # to: 买多
    def long(self, symbol, contract, amount, price, match_trade=False, lever_rate=10):
        return self.trade(
            symbol=symbol,
            contract=contract,
            price=price,
            amount=amount,
            order_type=1,
            match_trade=match_trade,
            lever_rate=lever_rate
        )

    # to: 买空
    def short(self, symbol, contract, amount, price, match_trade=False, lever_rate=10):
        return self.trade(
            symbol=symbol,
            contract=contract,
            price=price,
            amount=amount,
            order_type=2,
            match_trade=match_trade,
            lever_rate=lever_rate
        )

    # to: 平多
    def close_long(self, symbol, contract, amount, price, match_trade=False, lever_rate=10):
        return self.trade(
            symbol=symbol,
            contract=contract,
            price=price,
            amount=amount,
            order_type=3,
            match_trade=match_trade,
            lever_rate=lever_rate
        )

    # to: 平空
    def close_short(self, symbol, contract, amount, price, match_trade=False, lever_rate=10):
        return self.trade(
            symbol=symbol,
            contract=contract,
            price=price,
            amount=amount,
            order_type=4,
            match_trade=match_trade,
            lever_rate=lever_rate
        )

    # to: 市价买多
    def long_on_match(self, symbol, contract, amount, lever_rate=10):
        return self.long(symbol, contract, amount, 0, True, lever_rate=lever_rate)

    # to: 市价买空
    def short_on_match(self, symbol, contract, amount, lever_rate=10):
        return self.short(symbol, contract, amount, 10000, True, lever_rate=lever_rate)

    # to: 市价平多
    def close_long_on_match(self, symbol, contract, amount, lever_rate=10):
        return self.close_long(symbol, contract, amount, 10000, True, lever_rate=lever_rate)

    # to: 市价平空
    def close_short_on_match(self, symbol, contract, amount, lever_rate=10):
        return self.close_short(symbol, contract, amount, 0, True, lever_rate=lever_rate)

    # ------------------------------------------------------------ #

    @staticmethod
    def __make_every_value_str(parameters):
        for key in parameters:
            parameters[key] = str(parameters[key])
        return parameters

    # def __ws_msg(self, message):
    #     self.ws.send(message)
    #     result = self.ws.recv()
    #     print result
    #     return result

    def __make_trade_parameters(self, symbol, contract, price, amount, order_type, match_trade=False, lever_rate=10):
        parameters_temp = {
            'api_key': self.API_KEY,
            'symbol': symbol,
            'contract_type': contract,
            'price': price,
            'amount': amount,
            'type': order_type,
            'match_price': 1 if match_trade else 0,
            'lever_rate': lever_rate
        }

        signature = sign(params=parameters_temp, secretKey=self.SECRET)
        parameters_temp['sign'] = signature

        parameters = self.__make_every_value_str(parameters_temp)

        return parameters

    def __make_cancel_parameters(self, symbol, contract, order_id):
        parameters_temp = {
            'api_key': self.API_KEY,
            'symbol': symbol,
            'order_id': order_id,
            'contract_type': contract
        }

        signature = sign(params=parameters_temp, secretKey=self.SECRET)
        parameters_temp['sign'] = signature

        parameters = self.__make_every_value_str(parameters_temp)

        return str({
            'event': 'addChannel',
            'channel': 'ok_futureusd_cancel_order',
            'parameters': parameters,
        })


##
