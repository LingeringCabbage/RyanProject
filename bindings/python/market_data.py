import json
import os
import time
import threading
from dotenv import load_dotenv
from typing import List, Callable

from polygon import RESTClient

load_dotenv()
POLYGON_API_KEY = os.getenv("API_KEY")


class MarketData:
    def __init__(self):
        self.client = RESTClient(api_key=POLYGON_API_KEY)
        self.tickers = []
        self.image_paths = []
        self.tickers_data = []

    def get_market_data(self, symbol, start_date, end_date):
        """
        Get market data for a given symbol and date range
        """
        return self.client.get_aggs(symbol, 1, "day", start_date, end_date)
    
    def load_tickers_background(self, tickers: List[str]):
        """Super simple version - just start and forget"""
        def _load():
            tickers_data = []
            for i, ticker in enumerate(tickers):
                if i > 0 and i % 5 == 0:
                    print("Sleeping for 60 seconds")
                    time.sleep(60)
                print(f"Loading {ticker}...")
                tickers_data.append(self.get_market_data(ticker, "2025-06-03", "2025-06-04"))
            # callback(tickers_data)
            self.tickers_data = tickers_data
        
        threading.Thread(target=_load, daemon=True).start()

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