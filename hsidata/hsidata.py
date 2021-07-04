from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, datetime, json, os

path = r'C:\Users\s1113\Desktop\hsidata\chromedriver.exe'

class StockPrice:
    def __init__(self, stock_code): 
        self.driver = webdriver.Chrome(executable_path=path)
        self.stock_code = stock_code
        self.driver.get('http://www.aastocks.com/tc/')
        inputbox = self.driver.find_element_by_id('sb-txtSymbol-aa') 
        inputbox.send_keys(self.stock_code)
        inputbox.send_keys(Keys.ENTER)

    def get_price(self):
        time.sleep(3)

        timestamp = str(datetime.datetime.now())
        layout = self.driver.find_element_by_class_name('lastBox')
        text = layout.find_element_by_class_name('neg').get_attribute('innerHTML')
        price = text.split('</span>')[1]
        
        data = {
            'Stock': self.stock_code,
            'Time' : timestamp,
            'Price': price
        }

        print(data)
        self.driver.refresh()
        return data
    
bot = StockPrice(700)

while True:
    mydata = []
    fn = f'{bot.stock_code}.json'

    if os.path.isfile(fn):
        with open(fn) as fp:
            mydata = json.load(fp)

    new_data = bot.get_price()
    mydata.append(new_data)

    with open(fn, 'w') as fp:
        json.dump(mydata, fp)