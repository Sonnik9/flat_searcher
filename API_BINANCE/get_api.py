# import time
# import random
from datetime import datetime
import pandas as pd
import asyncio
import time
from connectorss import CONNECTOR_TG
import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)

method = 'GET'

class GETT_API_CCXT(CONNECTOR_TG):
    def __init__(self):   
        super().__init__()     

    async def get_ccxtBinance_klines(self, symbol, timeframe, limit):

        retry_number = 3
        decimal = 1.1        
        for i in range(retry_number):
            try:
                klines = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                data = pd.DataFrame(klines, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                data['Time'] = pd.to_datetime(data['Time'], unit='ms')
                data.set_index('Time', inplace=True)
                data = data.astype(float)
                return data
            except Exception as e:
                print(f"Error fetching klines: {e}")
                # time.sleep(1)
                await asyncio.sleep(1.1 + i*decimal)     

        return pd.DataFrame()

class GETT_API(GETT_API_CCXT):

    def __init__(self) -> None:
        super().__init__()   
        
    async def get_all_tickers(self):

        all_tickers = None
        url = self.URL_PATTERN_DICT['all_tikers_url']        
        all_tickers = await self.HTTP_request(url, method=method, headers=self.header)

        return all_tickers
    
    async def get_excangeInfo(self, symbol):       

        exchangeInfo = None
        if symbol:            
            url = f"{self.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"
        else:
            url = self.URL_PATTERN_DICT['exchangeInfo_url']        
        exchangeInfo = await self.HTTP_request(url, method=method, headers=self.header)

        return exchangeInfo

# # //////////////////////////////////////////////////////////////////////////////////

# get_apii = GETT_API()
# symbol = 'BNBUSDT'
# symbol = 'SOLUSDT'
# klines = asyncio.run(get_apii.get_klines(symbol, '1m', 30))
# print(klines)
# klines = asyncio.run(get_apii.get_ccxtBinance_klines(symbol, '1m', 30))
# print(klines)
# price = asyncio.run(get_apii.get_current_price(symbol))
# open_pos = asyncio.run(get_apii.get_open_positions())
# print(open_pos)
# print(price)
