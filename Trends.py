from pprint import pprint
from os import path
import requests
import time

import pandas as pd

pd.options.display.max_columns = 100

INTERVAL = 60*60 #Interval in seconds 

class Trends:
    fileName = "Trends.csv"
    url = 'https://api.coinmarketcap.com/data-api/v3/topsearch/rank?timeframe=24h&top=30'
    datatime = None
    startTime = None

    def __init__(self):
        self.startTime = time.strftime("%d-%m-%Y %Hh %Mm %Ss", time.gmtime())

    def formatTrend(self, trend):
        try:
            return {
                'Time': self.datatime,
                'Id': trend['id'],
                "MarketCap": trend['marketCap'],
                "Name": trend['name'],
                "Price": trend['priceChange']['price'],
                'PriceChange24h': trend['priceChange']['priceChange24h'],
                'PriceChange30d': trend['priceChange']['priceChange30d'],
                'PriceChange7d': trend['priceChange']['priceChange7d'],
                'Volume24h': trend['priceChange']['volume24h'],
                'Rank': None if not 'rank' in trend else trend['rank'],
                'Slug': trend['slug'],
                'Status': trend['status'],
                'Symbol': trend['symbol']
            }
        except:
            print("Format error")
        return None

    def updateTrends(self):
        try:
            r = requests.get(self.url)
            data = r.json()
            self.datatime = data['status']['timestamp']

            data = list(
                map(self.formatTrend, data['data']['cryptoTopSearchRanks']))
            dataframe = pd.DataFrame(data=data, columns=['Time', 'Id', 'MarketCap', 'Name', 'Price', 'PriceChange24h',
                                                         'PriceChange30d', 'PriceChange7d', 'Volume24h', 'Rank', 'Slug', 'Status', 'Symbol'])

            if(path.exists("./Trends/"+self.fileName)):
                historical = pd.read_csv("./Trends/"+self.fileName)
                dataframe = pd.concat(
                    [historical, dataframe], ignore_index=True)
            dataframe.to_csv("./Trends/"+self.fileName, index=False)
            print("Save: "+self.fileName)
        except:
            print("Update failed")


trends = Trends()
while True:
    print("Saving "+time.strftime("%T", time.gmtime()))
    trends.updateTrends()
    time.sleep(INTERVAL)
