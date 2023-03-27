import threading

import requests
from bs4 import BeautifulSoup
from tkinter import *


def collect_stock_info(root, stockInputField, targetPriceInputField):
    # Collect stocks from input field
    listOfStocksBeingScraped = stockInputField.get()
    listOfStocksBeingScraped = listOfStocksBeingScraped.split(',')

    print(listOfStocksBeingScraped)

    # Collect target prices from input field
    listOfTargetPrices = targetPriceInputField.get()
    listOfTargetPrices = listOfTargetPrices.split(',')

    def scrape_stock_info(stockBeingScraped, index):
        # Adds the stock being scraped from the stock list to the url
        url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')

        # Requests and bs4
        request = requests.get(url)
        result = BeautifulSoup(request.text, 'html.parser')

        try:
            # Find the stock name
            stockName = (result.find('div', {'class': 'zzDege'})).string

        except AttributeError:
            print('Name not found on google.com/finance')
            return

        # Find the stock price
        stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string

        print(stockName, stockPrice)

        def create_stock_info_label(root):
            stock_info_label = Label(root, text=f'{stockName}: {stockPrice}')
            stock_info_label.grid(row=3 + index, column=1, sticky='nsew')

        create_stock_info_label(root)

    for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
        scrape_stock_info_thread = threading.Thread(target=scrape_stock_info, args=(stockBeingScraped, index))
        scrape_stock_info_thread.start()
        root.update_idletasks()
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

