import requests
import lxml.html
from selenium import webdriver
from selenium.webdriver.common.by import By
from forex_python.converter import CurrencyRates
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import quote
import pandas as pd
import time
import json


class Scraper:

    def ScrapingPopularItemSteamMarket(self):
        html = requests.get("https://steamcommunity.com/market/")
        doc = lxml.html.fromstring(html.content)

        popular_items = doc.xpath('//div[@id="popularItemsRows"]')

        popular_items = doc.xpath('//div[@id="popularItemsRows"]')[0]

        self.titles = popular_items.xpath('.//span[@class="market_listing_item_name"]/text()')



    def ScrapingPrices(self):
        html_urls_list = [quote(name) for name in self.titles]
        # html_urls_list = ["Dreams%20%26%20Nightmares%20Case"]
        

        self.prices = []
        
        
       
        driver = webdriver.Chrome()

    

        for item in html_urls_list:
            try:
                driver.get(f'https://steamcommunity.com/market/listings/730/{item}')
                time.sleep(5)

                element = driver.find_element(By.XPATH, '//div[@id="market_commodity_buyrequests"]')
                prices = element.find_elements(By.XPATH, './/span[@class="market_commodity_orders_header_promote"]')
                prices_text = [price.text for price in prices]
                real_price = prices_text[1]
                self.prices.append(real_price)
          
                
            

            except NoSuchElementException as e:
                print("Element not found, trying app ip 440")

                driver.get(f'https://steamcommunity.com/market/listings/440/{item}')
                time.sleep(5)

                element = driver.find_element(By.XPATH, '//div[@id="market_commodity_buyrequests"]')
                prices = element.find_elements(By.XPATH, './/span[@class="market_commodity_orders_header_promote"]')
                prices_text = [price.text for price in prices]
                real_price = prices_text[1]
                self.prices.append(real_price)


            except Exception as e:
                print(f"An unexpected error occurred")
                driver.get(f'https://steamcommunity.com/market/listings/730/{item}')
                time.sleep(5)

                element = driver.find_element(By.XPATH, '//div[@id="market_commodity_buyrequests"]')
                prices = element.find_elements(By.XPATH, './/span[@class="market_commodity_orders_header_promote"]')
                prices_text = [price.text for price in prices]
                real_price = prices_text[1]
                self.prices.append(real_price)



        driver.quit()
                
                
        # print(self.prices)

    def usd_to_sgd(self):
            self.converted_currency = []

    
            # amount = ['$1.70', '$0.73', '$1.44', '$0.63', '$0.89', '$2.32', '$0.97', '$0.37', '$5.38', '$7.13']

            c = CurrencyRates()
            exchange_rate = c.get_rate('USD', 'SGD')

            currency_float = [float(value[1:]) for value in self.prices]

            for i in currency_float:
                result = i * exchange_rate
                after_steam_tax = (result / 115) * 100
                rounded_result = round(after_steam_tax, 2)
                self.converted_currency.append(rounded_result)
            

            




    def save_title_and_price(self):
        json_file_path = 'data.json'

        data = {'name': self.titles, 'price': self.converted_currency}

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)   
     



    def open_load_json(self):
            with open('data.json', 'r') as json_file:
                loaded_data = json.load(json_file)

            return loaded_data


        

    def menu(self):

        print("Welcome to W1nnie's Steam case checker thing")
        print("Do not run the scraper too many times, Steam will rate limit you")
        
        loop = True 

        while loop is True:
            print("1) Run Web scraper to collect price")
            print("2) Analyse case with game price")
            
            choice = int(input(":"))

            if choice == 1:
                print("Running Web Scraper")
                print("The scraper might crash. If it does, just rerun it")
                self.ScrapingPopularItemSteamMarket()

                self.ScrapingPrices()

                self.usd_to_sgd()

                self.save_title_and_price()

                print("OK Web scraping completed")
                print("")




            if choice == 2:
                c = CurrencyRates()
                
                print("Enter the price of the game in lira")   
                loop = True
                
                while loop is True:
                    self.game_price_in_lira = int(input(": "))

                    if self.game_price_in_lira < 1:
                        print("Invalid option buddy, read again")

                    else:
                        loop = False


                exchange_rate2 = c.get_rate('TRY', 'SGD')
                result2 = self.game_price_in_lira * exchange_rate2
                self.game_price_converted_to_SGD = round(result2, 2)
        

        self.Calcu_quant_cases_to_price()

        data = self.open_load_json()
        loaded_price = data['price']
        loaded_titles = data['name']

        values_with_SGD = ['SGD {}'.format(value) for value in loaded_price]

        zipped_data = zip(loaded_titles, values_with_SGD, self.quant_of_cases)

                
        print("Price of game converted to SGD: ", self.game_price_converted_to_SGD)
        print("")
        print("Case                           ", "Price of case    ", "Quantity of cases need to match price of game")
        for row in zipped_data:
            print("{:<32} {:<18} {:<20}".format(*row))
        
        input("Press Enter to Close")




    def Calcu_quant_cases_to_price(self):
        self.quant_of_cases = []
        
        data =  self.open_load_json()
        loaded_price = data['price']

        for i in loaded_price:
            quant = self.game_price_converted_to_SGD / i
            r_quant = round(quant, 1)  
            self.quant_of_cases.append(r_quant)






    def __init__(self):

        self.menu()
    
    


Scraper()