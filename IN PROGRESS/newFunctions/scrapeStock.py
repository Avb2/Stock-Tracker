import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from tkinter import *


def collect_stock_info(root, stockInputField, targetPriceInputField, lock):
    lock.acquire()
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

        # Find the previous closing price
        stockPreviousClosingPrice = result.find('div', {'class': 'P6K39c'}).string

        def create_stock_info_labels(root):
            timeDateTitleLabel = Label(root, text='Date/Time', borderwidth=1.5, relief='solid', font=('Arial', 16))
            timeDateTitleLabel.grid(row=3, column=1, sticky='nsew')

            stockTitleLabel = Label(root, text='Name', borderwidth=1.5, relief='solid', font=('Arial', 16))
            stockTitleLabel.grid(row=3, column=2, sticky='nsew')

            priceTitleLabel = Label(root, text='Price', borderwidth=1.5, relief='solid', font=('Arial', 16))
            priceTitleLabel.grid(row=3, column=3, sticky='nsew')

            closingPriceTitleLabel = Label(root, text='Closing Price', borderwidth=1.5, relief='solid', font=('Arial', 16))
            closingPriceTitleLabel.grid(row=3, column=4, sticky='nsew')

            currentTimeDateLabel = Label(root, text=f'{str(datetime.now())[:11]} : {str(datetime.now())[11:16]}', font=('Arial', 16))
            currentTimeDateLabel.grid(row=4 + index, column=1, sticky='nsew')

            stockNameLabel = Label(root, text=f'{stockName}: ', font=('Arial', 16))
            stockNameLabel.grid(row=4 + index, column=2, sticky='nsew')

            stockPriceLabel = Label(root, text=stockPrice, font=('Arial', 16))
            stockPriceLabel.grid(row=4 + index, column=3, sticky='nsew')

            stockPreviousClosingPriceLabel = Label(root, text=stockPreviousClosingPrice, font=('Arial', 16))
            stockPreviousClosingPriceLabel.grid(row=4 + index, column=4, sticky='nsew')

            # Adds padding between all rows of stock information
            for num in range(index):
                root.rowconfigure(num + 4, pad=10)


        create_stock_info_labels(root)

    for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
        scrape_stock_info_thread = threading.Thread(target=scrape_stock_info, args=(stockBeingScraped, index))
        scrape_stock_info_thread.start()
    lock.release()



