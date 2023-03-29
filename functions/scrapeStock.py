import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from tkinter import *
from functions.databaseQuerying import add_to_db
from functions.modelStocks import showPlot


def collect_stock_info(root, stockInputField, targetPriceInputField, lock):
    lock.acquire()
    # Collect stocks from input field
    listOfStocksBeingScraped = stockInputField.get()
    listOfStocksBeingScraped = listOfStocksBeingScraped.split(',')

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

        SearchedBy = []
        # What the user searched the stock by
        for theStock in listOfStocksBeingScraped:
            SearchedBy += [theStock.lower()]

        # Find the previous closing price
        stockPreviousClosingPrice = result.find('div', {'class': 'P6K39c'}).string

        def collect_time():
            # Get timestamp
            time = str(datetime.now())[11:16]
            return time

        def collect_date():
            date = str(datetime.now())[:11]
            return date

        def create_graph_button(root):
            buttonGraphPrices = Button(root, text='Graph', command=lambda: showPlot(stockName))
            buttonGraphPrices.grid(row=5 + index, column=5)

        def create_stock_info_labels(root):
            time = collect_time()
            date = collect_date()

            # Time/ Date Title label
            timeDateTitleLabel = Label(root, text='Date/Time', borderwidth=1.5, relief='solid', font=('Arial', 16))
            timeDateTitleLabel.grid(row=4, column=1, sticky='nsew')

            # Stock Title label
            stockTitleLabel = Label(root, text='Name', borderwidth=1.5, relief='solid', font=('Arial', 16))
            stockTitleLabel.grid(row=4, column=2, sticky='nsew')

            # Price Title label
            priceTitleLabel = Label(root, text='Price', borderwidth=1.5, relief='solid', font=('Arial', 16))
            priceTitleLabel.grid(row=4, column=3, sticky='nsew')

            # Closing price Title label
            closingPriceTitleLabel = Label(root, text='Closing Price', borderwidth=1.5, relief='solid', font=('Arial', 16))
            closingPriceTitleLabel.grid(row=4, column=4, sticky='nsew')

            # Displays current time/date
            currentTimeDateLabel = Label(root, text=f'{date} : {time}', font=('Arial', 16))
            currentTimeDateLabel.grid(row=5 + index, column=1, sticky='nsew')

            # Displays stock name
            stockNameLabel = Label(root, text=f'{stockName}: ', font=('Arial', 16))
            stockNameLabel.grid(row=5 + index, column=2, sticky='nsew')

            # Displays stock price
            stockPriceLabel = Label(root, text=stockPrice, font=('Arial', 16))
            stockPriceLabel.grid(row=5 + index, column=3, sticky='nsew')

            # Displays Previous closing price
            stockPreviousClosingPriceLabel = Label(root, text=stockPreviousClosingPrice, font=('Arial', 16))
            stockPreviousClosingPriceLabel.grid(row=5 + index, column=4, sticky='nsew')

            # Adds padding between all rows of stock information
            for num in range(index):
                root.rowconfigure(num + 4, pad=10)

        create_stock_info_labels(root)

        time = collect_time()
        date = collect_date()

        add_to_db(SearchedBy=SearchedBy[index], name=stockName, priceFloat=float(stockPrice.replace('$', '')), date=date, time=time, targetPrice=listOfTargetPrices[index])
        create_graph_button(root)

    for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
        scrape_stock_info_thread = threading.Thread(target=scrape_stock_info, args=(stockBeingScraped, index))
        scrape_stock_info_thread.start()
    lock.release()



