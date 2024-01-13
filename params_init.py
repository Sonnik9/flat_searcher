import os
import asyncio
import logging, os, inspect
from dotenv import load_dotenv
logging.basicConfig(filename='API_BINANCE/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

load_dotenv()

class BASIC_PARAMETRS():
    def __init__(self):        
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'      
        self.market = 'futures'
        self.test_flag = False
        
    def init_api_key(self):
        self.tg_api_token = os.getenv("TG_API_TOKEN", "")
        self.api_key  = os.getenv(f"BINANCE_API_PUBLIC_KEY__TESTNET_{str(self.test_flag)}", "")
        self.api_secret = os.getenv(f"BINANCE_API_PRIVATE_KEY__TESTNET_{str(self.test_flag)}", "")  

        self.header = {
            'X-MBX-APIKEY': self.api_key
        }     

class URL_TEMPLATES(BASIC_PARAMETRS):
    def __init__(self) -> None:
        super().__init__()        
        self.URL_PATTERN_DICT= {}              

    def init_urls(self):  
        if not self.test_flag:     
        
            self.URL_PATTERN_DICT['current_ptice_url'] = "https://fapi.binance.com/fapi/v1/ticker/price"
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://fapi.binance.com/fapi/v1/order'
            self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://fapi.binance.com/fapi/v2/balance'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://fapi.binance.com/fapi/v1/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://fapi.binance.com/fapi/v2/positionRisk'
            self.URL_PATTERN_DICT["set_leverage_url"] = 'https://fapi.binance.com/fapi/v1/leverage'
            self.URL_PATTERN_DICT["klines_url"] = 'https://fapi.binance.com/fapi/v1/klines'
            self.URL_PATTERN_DICT["set_margin_type_url"] = 'https://fapi.binance.com/fapi/v1/marginType'

        else:
            print('futures test')
            self.URL_PATTERN_DICT['current_ptice_url'] = "https://testnet.binancefuture.com/fapi/v1/ticker/price"
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://testnet.binancefuture.com/fapi/v1/order'            
            self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://testnet.binancefuture.com/fapi/v1/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://testnet.binancefuture.com/fapi/v2/balance'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/allOpenOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://testnet.binancefuture.com/fapi/v2/positionRisk'
            self.URL_PATTERN_DICT["set_leverage_url"] = 'https://testnet.binancefuture.com/fapi/v1/leverage'
            self.URL_PATTERN_DICT["klines_url"] = 'https://testnet.binancefuture.com/fapi/v1/klines'
            self.URL_PATTERN_DICT["set_margin_type_url"] = 'https://testnet.binancefuture.com/fapi/v1/marginType'

    
class TIME_TEMPLATES(URL_TEMPLATES):   
    def __init__(self) -> None:
        super().__init__()
        self.KLINE_TIME, self.TIME_FRAME = 15, 'm'
        self.INTERVAL = str(self.KLINE_TIME) + self.TIME_FRAME


class FILTER_SET(TIME_TEMPLATES):
    def __init__(self) -> None:
        super().__init__()
        self.SLICE_VOLUME_PAIRS = 100 # volums
         
        # self.SLICE_VOLATILITY = 200 # volatility
        self.MIN_FILTER_PRICE = 0.0001 # min price
        self.MAX_FILTER_PRICE = 3000000 # max price
        
        # self.problem_pairs = ['DOGEUSDT'] # problem coins list
        self.problem_pairs = ['USDCUSDT'] 
        self.MIN_VOLUM_USDT = 50000

class INDICATRS_SETTINGS(FILTER_SET):
    def __init__(self) -> None:
        super().__init__()
        self.BB_stddev_MULTIPLITER = 2.5
        self.KC_stddev_MULTIPLITER = 1.5

class TG_HANDLER_VARS(INDICATRS_SETTINGS):
    def __init__(self) -> None:
        super().__init__()

    def init_handler_vars(self):
        self.lock_candidate_coins = asyncio.Lock() 
        self.pump_candidate_set = set()   

        self.stop_triger_flag = False  
        self.settings_tg_flag = False
        self.settings_1_redirect_flag = False
        self.launch_finish_text = None


class INIT_PARAMS(TG_HANDLER_VARS):
    def __init__(self) -> None:
        super().__init__()
        self.init_itits()

    def init_itits(self):
        print('helloo')
        self.init_api_key()       
        self.init_urls()
        self.init_handler_vars()



# python constructorr.py
