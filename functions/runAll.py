import threading
from datetime import datetime
from tkinter import *
from functions.databaseQuerying import add_to_db, establish_db_connection
from functions.modelStocks import showPlot
from functions.scrapeStock import create_stock_info_labels, request_and_parse


def run_all_stocks(root, lock):
    def get_combobox_values():
        # Connect to sqlite db
        c = establish_db_connection()

        # Collects all table names from the sqlite database and creates a tuple
        c[0].execute(f'SELECT SearchedBy FROM AllStocks')
        allStocksTuple = c[0].fetchall()

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
        result = request_and_parse(url)

        try:
            # Find the stock name
            stockName = (result.find('div', {'class': 'zzDege'})).string

        except AttributeError:
            # If the stock name cannot be found, the name of the stock and the url will be displayed in the
            # console with a 'Name Not Found' message and will iterate to the next stock
            print('Name not found on google.com/finance')
            return

        # Find the stock price
        stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string

        print(stockName, stockPrice)

        # Sets searchedBy equal to the stockBeingScraped for readability
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

        create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index)

        time = collect_time()
        date = collect_date()

        add_to_db(SearchedBy=SearchedBy, name=stockName, priceFloat=float(stockPrice.replace('$', '')), date=date,
                  time=time, targetPrice=0)

        return comboBoxValues

    lock.acquire()

    comboBoxValues = get_combobox_values()

    for index, stockBeingScraped in enumerate(comboBoxValues):
        print(stockBeingScraped)
        scrape_stock_info_thread = threading.Thread(target=run_all_scrape_stocks, args=(index, stockBeingScraped))
        scrape_stock_info_thread.start()

    lock.release()
