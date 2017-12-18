# encoding: utf-8

import threading
import time
import urllib
import hashlib
import requests
from urlparse import urljoin


import pandas as pd

# to: 工具函数 简易的多线程工具
class Ironman(object):
    @classmethod
    def thread(cls, target, args=None, name=None):
        if args is None:
            args = {}
        this_thread = threading.Thread(target=target, name=name, args=args)
        this_thread.start()

    @classmethod
    def to_datetime(cls, absolute_timestamp):
        return pd.to_datetime(absolute_timestamp, unit="s")

    @classmethod
    def now_datetime(cls):
        return cls.to_datetime(time.time())

    @classmethod
    def sprint(cls, speaker="某人", string=""):
        print cls.now_datetime(), speaker, "：", ">>>", string

    @classmethod
    def sign(cls, params, secretKey):
        sign = ''
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) + '&'
        data = sign + 'secret_key=' + secretKey
        result = hashlib.md5(data.encode("utf8")).hexdigest().upper()
        return result

    @classmethod
    def httpGet(cls, url, resource, params=''):
        r = requests.get(url + resource + '?' + params, timeout=10)
        try:
            return r.json()
        except ValueError as e:
            print(r.text)
            raise

    @classmethod
    def httpPost(cls, url, resource, params):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }

        url = urljoin(url, resource)
        params = urllib.urlencode(params)
        r = requests.post(url, headers=headers, data=params, timeout=10)
        try:
            return r.json()
        except ValueError as e:
            print(r.text)
            raise
