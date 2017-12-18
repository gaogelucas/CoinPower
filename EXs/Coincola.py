import requests
from bs4 import BeautifulSoup

##

class Coincola(object):
    def __init__(self):
        self.to_sell_url = "https://www.coincola.com/sell?country_code=CN"
        self.to_buy_url = "https://www.coincola.com/sell?country_code=CN"

    def get_bids(self):
        r = requests.get(self.to_sell_url)
        soup = BeautifulSoup(r.text)
        