import requests
from bs4 import BeautifulSoup
from time import sleep

class BaseSite(object):
    
    def getParsed(self, url ):
        for _ in range(10):
            try:
                page = requests.get(url)
            except requests.exceptions.ConnectionError as e:
                sleep(60)
        doc = BeautifulSoup(page.text)
        return doc