from lbcapi import api
import pandas as pd
import json

class LocalBitcoins(object):
    def __init__(self):
        self.read_key = "135c16bffc3530dd9d6c4f6e6cf8c333"
        self.write_key = "458e4fb85f7be77bec9f3484b0f5b76c"
        self.money_key = "c9a8cd8906731ebaac57853cac159da6"
        self.money_pin_key = "cca4d8e16f5a18ae9d081a553da4efe3"

        self.read_sn = "242be49c0d1dc395c8c7ac36cfe18bcab545f600d47bb23d7d21da00042f79ec"
        self.write_sn = "2f285d6d0f46541e121eb9d463fee7011b52526f6c824c0f222aa69719f3f5db"
        self.money_sn = "c7a0b43616bf1c0f995846a1393045d1fbf19f5b751cc7b2a3d277348c1e0356"
        self.money_pin_sn = "e978ce1c81fca602237a2af6e94e2ecfa29bcdc80d0e747e05686d5f86498cb1"

        self.conn = self.connect()

    def connect(self):
        return api.hmac(self.read_key, self.read_sn)

##
a = LocalBitcoins()
a.conn.call('GET', '/buy-bitcoins-online/CNY/alipay/.json').json()
a.conn.call('GET', '/sell-bitcoins-online/CNY/alipay/.json').json()