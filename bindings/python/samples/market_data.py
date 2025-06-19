import json
import os
import time
import threading
from dotenv import load_dotenv
from typing import List, Callable

from polygon import RESTClient
from finnhub import Client

load_dotenv()
# POLYGON_API_KEY = os.getenv("API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


class MarketData:
    def __init__(self):
        self.client = Client(api_key=FINNHUB_API_KEY)
        self.tickers = []
        self.tickers_data = []

    def get_market_data(self, symbol):
        """
        Get market data for a given symbol and date range
        """
        # return self.client.get_aggs(symbol, 1, "day", start_date, end_date)
        return self.client.quote(symbol)
    
    def load_tickers_background(self, tickers: List[str]):
        """Super simple version - just start and forget"""
        def _load():
            tickers_data = []
            for i, ticker in enumerate(tickers):
                if i > 0 and i % 50 == 0:
                    time.sleep(60)
                # print(f"Loading {ticker}...")
                curr_data = self.get_market_data(ticker)
                if curr_data["d"] is None:
                    tickers_data.append(("RYTARD", "TOUCH", "ME"))
                else:
                    curr_price = round(curr_data["c"], 2)
                    curr_difference = round(curr_data["d"], 2)
                    tickers_data.append((ticker, str(curr_price), str(curr_difference)))
            # callback(tickers_data)
            self.tickers_data = tickers_data
        
        thread = threading.Thread(target=_load, daemon=True)
        thread.start()
        return thread   # Return the thread so we can join it later

    # def load_tickers_background(self, tickers: List[str], callback: Callable):
    #     load_tickers_background(tickers, callback)


# market_data = MarketData()

# def process_data(data):
#     print(f"Got {len(data)} tickers!")
#     market_data.tickers_data = data


# [("path_to_aapl"), ("path_to_msft"), ("path_to_goog"), ("path_to_amzn"), ("path_to_tsla")]

# market_data.load_tickers_background(["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"])
# # with open("market_data.json", "w") as f:
# #     f.write(json.dumps(market_data.tickers_data, indent=4))
# time.sleep(3)
# print(market_data.tickers_data)

# i = 0
# while True:
#     if i == 10:
#         load_tickers_background(["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA"], process_data)
#     print(len(market_data.tickers_data))
#     i += 1
#     time.sleep(.25)
