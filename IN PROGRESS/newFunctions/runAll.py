import sqlite3
import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from tkinter import *
from newFunctions.databaseQuerying import add_to_db


def run_all_stocks(root, lock):
    lock.acquire()

    def get_combobox_values():
        # Connect to sqlite db
        connectionPool = sqlite3.connect('new-data-stocks.db')
        c = connectionPool.cursor()

        # Collects all table names from the sqlite database and creates a tuple
        c.execute(f'SELECT SearchedBy FROM AllStocks')
        allStocksTuple = c.fetchall()

        allStocks = []

        # Adds the value to the drop down box if the value is not already on the list
        for COUNT, x in enumerate(allStocksTuple):
            if x not in allStocks:
                allStocks += [x]

        # Converted tuple to list
        comboboxValuesList = []
        for values in allStocks:
            comboboxValuesList += list(values)

        return comboboxValuesList

    def run_all_scrape_stocks(index, stockBeingScraped):
        # List of all values from combobox
        comboBoxValues = get_combobox_values()

        # Adds the stock being scraped from the stock list to the url
        url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')
        print(url)

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

        SearchedBy = stockBeingScraped

        # Find the previous closing price
        stockPreviousClosingPrice = result.find('div', {'class': 'P6K39c'}).string

        def collect_time():
            # Get timestamp
            time = str(datetime.now())[11:16]
            return time

        def collect_date():
            date = str(datetime.now())[:11]
            return date

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
            closingPriceTitleLabel = Label(root, text='Closing Price', borderwidth=1.5, relief='solid',
                                           font=('Arial', 16))
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

        add_to_db(SearchedBy=SearchedBy, name=stockName, priceFloat=float(stockPrice.replace('$', '')), date=date,
                  time=time, targetPrice=0)

        return comboBoxValues

    comboBoxValues = get_combobox_values()

    for index, stockBeingScraped in enumerate(comboBoxValues):
        print(stockBeingScraped)
        scrape_stock_info_thread = threading.Thread(target=run_all_scrape_stocks, args=(index, stockBeingScraped))
        scrape_stock_info_thread.start()
    lock.release()
