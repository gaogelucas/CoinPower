#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类

import urllib
import hashlib
import requests
from urlparse import urljoin

def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    result = hashlib.md5(data.encode("utf8")).hexdigest().upper()
    return result

def httpGet(url,resource,params=''):
    r = requests.get(url+ resource + '?' + params, timeout=10)
    try:
        return r.json()
    except ValueError as e:
        print(r.text)
        raise

def httpPost(url,resource,params):
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
    }

    url = urljoin(url, resource)
    params = urllib.urlencode(params)
    r = requests.post(url, headers=headers, data=params, timeout=10)
    try:
        return r.json()
    except ValueError as e:
        print(r.text)
        raise
 
