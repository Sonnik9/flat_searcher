from API_BINANCE.get_api import GETT_API 
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import asyncio
import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)

class UTILS_APII(GETT_API):

    def __init__(self) -> None:
        super().__init__()

    async def assets_filters_1(self):
        all_tickers = []
        top_pairs = []
        exclusion_contains_list = ['UP', 'DOWN', 'RUB', 'EUR']
        
        all_tickers = await self.get_all_tickers()    

        try:
            if all_tickers:
                usdt_filtered = [ticker for ticker in all_tickers if
                                ticker['symbol'].upper().endswith('USDT') and
                                not any(exclusion in ticker['symbol'].upper() for exclusion in exclusion_contains_list) and
                                (float(ticker['lastPrice']) >= self.MIN_FILTER_PRICE) and (
                                        float(ticker['lastPrice']) <= self.MAX_FILTER_PRICE)]

                sorted_by_volume_data = sorted(usdt_filtered, key=lambda x: float(x['quoteVolume']), reverse=True)
                sorted_by_volume_data = sorted_by_volume_data[:self.SLICE_VOLUME_PAIRS]

                top_pairs = [x['symbol'] for x in sorted_by_volume_data if x['symbol'] not in self.problem_pairs]
        except Exception as ex:
            logging.exception(
                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return top_pairs
    
    # /////////////////////////////////////////////////////////////////////////////////////////////////////




# self.MIN_VOLUM_DOLLARS

# utils_apii = UTILS_API() 

# # python -m API.orders_utils

# # ///////////////////////////////////////////////////////////////////////////////////////
    

# symbol_data = {'symbol': 'ETHUSDT', 'pair': 'ETHUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404800000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'ETH', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 2, 'quantityPrecision': 3, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0500', 'liquidationFee': '0.020000', 'marketTakeBound': '0.10', 'maxMoveOrderLimit': 10000, 'filters': [{'maxPrice': '95264.25', 'filterType': 'PRICE_FILTER', 'tickSize': '0.01', 'minPrice': '18.67'}, {'minQty': '0.001', 'stepSize': '0.001', 'maxQty': '10000', 'filterType': 'LOT_SIZE'}, {'filterType': 'MARKET_LOT_SIZE', 'stepSize': '0.001', 'minQty': '0.001', 'maxQty': '10000'}, {'filterType': 'MAX_NUM_ORDERS', 'limit': 200}, {'filterType': 'MAX_NUM_ALGO_ORDERS', 'limit': 10}, {'filterType': 'MIN_NOTIONAL', 'notional': '20'}, {'multiplierDown': '0.9000', 'filterType': 'PERCENT_PRICE', 'multiplierDecimal': '4', 'multiplierUp': '1.1000'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}
# lot_size_filter = next((item for item in symbol_data['filters'] if item['filterType'] == 'LOT_SIZE'), None)  
# notional = float(lot_size_filter['notional'])
# print(notional)