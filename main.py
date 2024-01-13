from API_BINANCE.utils_api import UTILS_APII
from TECHNIQUES.techniques_py import TECHNIQUESS
from datetime import datetime
import asyncio
import time
import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)


money_emoji = "💰"
rocket_emoji = "🚀"
lightning_emoji =  "⚡"
clock_emoji = "⌚"
film_emoji = "📼"
percent_emoji = "📶"
repeat_emoji = "🔁"
upper_trigon_emoji = "🔼"
lower_trigon_emoji = "🔽"
confirm_emoji = "✅"
link_emoji = "🔗"


class TG_ASSISTENT(UTILS_APII, TECHNIQUESS):

    def __init__(self):
        super().__init__()

    def connector_func(self, message, response_message):
        retry_number = 3
        decimal = 1.1       
        for i in range(retry_number):
            try:
                self.bot.send_message(message.chat.id, response_message)                
                return message.text
            except:
                time.sleep(1.1 + i*decimal)        
                   
        return None

    async def cur_dateTime(self):        
        current_time = time.time()        
        datetime_object = datetime.fromtimestamp(current_time)       
        formatted_time = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
        return str(formatted_time)

    async def date_of_the_month(self):        
        current_time = time.time()        
        datetime_object = datetime.fromtimestamp(current_time)       
        formatted_time = datetime_object.strftime('%d')
        return int(formatted_time)    
  
    async def squeeze_unMomentum_assignator(self):
        coins_in_squeezeOn_var = []
        top_coins = await self.assets_filters_1()
        print(f"len(top_coins): {len(top_coins)}")        
        timeframe = '1h'
        limit = 100
        random_sleep = 0.1
                         
        for symbol in top_coins:
            m15_data = None                      
            await asyncio.sleep(random_sleep)
            # print('tik')
            if self.stop_triger_flag:
                return []         

            try:
                m15_data = await self.get_ccxtBinance_klines(symbol, timeframe, limit)        
                m15_data = await self.squeeze_unMomentum(m15_data)
                if m15_data['squeeze_on'].iloc[-1]:                         
                    coins_in_squeezeOn_var.append(symbol)
            except Exception as ex:
                logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        # print(coins_in_squeezeOn_var)

        return coins_in_squeezeOn_var

class TG_BUTTON_HANDLER(TG_ASSISTENT):
    def __init__(self):
        super().__init__()

    async def stop_tgButton_handler(self, tasks):
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:            
            pass
        finally:
            await asyncio.sleep(3)
            return True
        
    async def go_tgButton_handler(self, message):
        print('ksdvksfhbvb')
        curDatee = None
        date_of_the_month_start = await self.date_of_the_month()        
        return_squeeze_unMomentum_assignator = None
        squeeze_searcing_flag = False
        coins_in_squeezeOn = []
        tasks = []        

        while True:
            # print("Before sleep1")
            await asyncio.sleep(1)
            # print("After sleep1")
            try:
                # /////////////////////////////////////////////////////////////////////////////////////        
                if self.stop_triger_flag and self.stop_triger_tumbler_flag:
                    self.stop_triger_tumbler_flag = False
                    print(' sfhdvbfkvb')
                    
                    if tasks:
                        stop_response = None
                        stop_response = await self.stop_tgButton_handler(tasks)
                        if stop_response:
                            self.stop_triger_flag = False
                            return "The robot was stopped!"
                    else:
                        self.stop_triger_flag = False
                        return "The robot was stopped!"    

                        
                # # /////////////////////////////////////////////////////////////////////////////////////
                if not squeeze_searcing_flag:                    
                    coins_in_squeezeOn = []
                    return_squeeze_unMomentum_assignator = None
                    squeeze_searcing_flag = True
                    task1 = [self.squeeze_unMomentum_assignator()]
                    tasks.append(task1)
                    return_squeeze_unMomentum_assignator = asyncio.gather(*task1)
                    
                if return_squeeze_unMomentum_assignator and return_squeeze_unMomentum_assignator.done():
                    result_squeeze_unMomentum_assignator = return_squeeze_unMomentum_assignator.result()
                    return_squeeze_unMomentum_assignator = None 
                    coins_in_squeezeOn = result_squeeze_unMomentum_assignator[0]
                    
                    print(f"Монеты в сжатии: {coins_in_squeezeOn}\n {len(coins_in_squeezeOn)} шт")
                    coins_in_squeezeOn_toStr = [str(x) + ' ___ ' + f"https://www.coinglass.com/tv/Binance_{x}" for x in coins_in_squeezeOn]
                    curDatee = await self.cur_dateTime()
                    tg_reply = '\n'.join(coins_in_squeezeOn_toStr) + '\n' + str(curDatee)
                    message.text = self.connector_func(message, tg_reply)
                    return "It is done!"
                # /////////////////////////////////////////////////////////////////////////////////////
 


                # print("Before sleep2")
                await asyncio.sleep(1)
                # print("After sleep2")

            except Exception as ex:
                logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

                
class TG_MANAGER(TG_BUTTON_HANDLER):
    def __init__(self):
        super().__init__()

    def run(self):          
        # ///////////////////////////////////////////////////////////////////////////////
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):

            self.init_itits()
            self.bot.send_message(message.chat.id, "Choose an option:", reply_markup=self.menu_markup)
        # ///////////////////////////////////////////////////////////////////////////////
        # ///////////////////////////////////////////////////////////////////////////////  

        @self.bot.message_handler(func=lambda message: message.text == "STOP")
        def stopp(message):
            self.stop_triger_flag = True
            self.stop_triger_tumbler_flag = True
        # ////////////////////////////////////////////////////////////////////// 
        # /////////////////////////////////////////////////////////////////////////////// 

        @self.bot.message_handler(func=lambda message: message.text == 'RESTART')
        def handle_restsrt(message):     
            
            self.init_itits()
            self.bot.send_message(message.chat.id, "Bot restart. Please, choose an option!:", reply_markup=self.menu_markup)
            self.stop_triger_flag = False 

        # ////////////////////////////////////////////////////////////////////////////////////////////////
        # ///////////////////////////////////////////////////////////////////////////////

        @self.bot.message_handler(func=lambda message: message.text == "SETTINGS")
        def settingss(message):            
            response_message = "Please select a settings options:\n1 - Market" 
            message.text = self.connector_func(message, response_message) 
            self.settings_tg_flag = True

        @self.bot.message_handler(func=lambda message: self.settings_tg_flag and message.text == "1")
        def settingss_redirect_1(message):           
            response_message = '1 - Spot;\n2 - Futures'
            message.text = self.connector_func(message, response_message) 
            self.settings_tg_flag = False
            self.settings_1_redirect_flag = True

        @self.bot.message_handler(func=lambda message: self.settings_1_redirect_flag)
        def settingss_redirect_1_testnet(message): 
            self.settings_1_redirect_flag = False          
            if message.text.strip() == '1':
                self.market = 'spot'
            elif message.text.strip() == '2':
                self.market = 'futures'
            self.init_api_key()       
            self.init_urls()
            response_message = f'Testnet flag was chenged on {self.market.upper()}'
            message.text = self.connector_func(message, response_message)           

        # ///////////////////////////////////////////////////////////////////////////////  

        @self.bot.message_handler(func=lambda message: message.text == "GO")
        def go(message):
            self.init_itits()
            response_message = "Please wait. It's gonna take some time...."
            message.text = self.connector_func(message, response_message)
            self.launch_finish_text = asyncio.run(self.go_tgButton_handler(message))
            message.text = self.connector_func(message, self.launch_finish_text)
            
            # async def go_async():
            #     self.launch_finish_text = await self.go_tgButton_handler(message)
            #     # self.launch_finish_text = asyncio.run(self.go_tgButton_handler(message))
            #     message.text = self.connector_func(message, self.launch_finish_text)
            #     self.go_inProcess_flag = False
            #     return
            # asyncio.run(go_async())

        # ///////////////////////////////////////////////////////////////////////////////////
            
        @self.bot.message_handler(func=lambda message: message.text not in self.reserved_frathes_list)
        def exceptions_input(message):
            response_message = f"Try again and enter a valid option."
            message.text = self.connector_func(message, response_message)                 

        self.bot.polling()

def main():
    my_bot = TG_MANAGER()
    my_bot.run()

if __name__=="__main__":
    main()
