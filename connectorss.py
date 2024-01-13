from params_init import INIT_PARAMS
import os
import telebot
from telebot import types
import time
import hmac
import hashlib
import requests
import ccxt
import logging, os, inspect
from dotenv import load_dotenv
logging.basicConfig(filename='API_BINANCE/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

load_dotenv()

class CONNECTOR_CCXT(INIT_PARAMS):
    def __init__(self):   
        super().__init__()     
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True, 
        })
        
class CONNECTOR_BINANCEE(CONNECTOR_CCXT):

    def __init__(self) -> None:
        super().__init__()

    def get_signature(self, params):
        try:
            params['timestamp'] = int(time.time() *1000)
            params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
            hash = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256)        
            params['signature'] = hash.hexdigest()
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

        return params
   
    async def HTTP_request(self, url, **kwards):

        response = None
        multipliter = 2

        for i in range(2):
            try:
                # print('hi')
                response = requests.request(url=url, **kwards)
                # print(response)
                if response.status_code == 200:
                    break
                else:
                    time.sleep((i+1) * multipliter)              
   
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                time.sleep((i+1) * multipliter)                
                
        try:
            response = response.json()
        except:
            pass

        return response
    
class CONNECTOR_TG(CONNECTOR_BINANCEE):
    def __init__(self):  
        super().__init__()      
        self.bot = telebot.TeleBot(self.tg_api_token)
        self.menu_markup = self.create_menu()
        self.reserved_frathes_list = ["SETTINGS", "GO", "STOP", "RESTART", "1", "2"]
        self.signal_number_acumm_list = []        

    def create_menu(self):
        menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        
        button1 = types.KeyboardButton("SETTINGS")   
        button2 = types.KeyboardButton("GO") 
        button3 = types.KeyboardButton("STOP") 
        button4 = types.KeyboardButton("RESTART")
        menu_markup.add(button1, button2, button3, button4)        
        return menu_markup
