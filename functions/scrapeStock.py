import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from tkinter import *
from functions.databaseQuerying import add_to_db
from functions.databaseQuerying import add_to_db_for_sectors
from functions.modelStocks import showPlot


def collect_time():
    # Get timestamp
    time = str(datetime.now())[11:16]
    return time


def collect_date():
    date = str(datetime.now())[:11]
    return date


def create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index):
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


def collect_stock_info(root, stockInputField, targetPriceInputField, lock):
    def scrape_stock_info_for_sectors(root, stockInputField):
        def scrape_sector_list(sector):
            for index, stockBeingScraped in enumerate(sector):
                # Adds the stock being scraped from the stock list to the url
                url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')

                # Requests and bs4
                request = requests.get(url)
                result = BeautifulSoup(request.text, 'html.parser')

                try:
                    # Find the stock name
                    stockName = (result.find('div', {'class': 'zzDege'})).string

                except AttributeError:
                    print(stockBeingScraped, url)
                    print('Name not found on google.com/finance')
                    continue

                # Find the stock price
                stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string

                print(stockName, stockPrice)

                SearchedBy = []

                # Find the previous closing price
                stockPreviousClosingPrice = result.find('div', {'class': 'P6K39c'}).string

                create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index)

                theTime = collect_time()
                date = collect_date()

                add_to_db_for_sectors(stockInputField.get(), stockName, date, theTime,
                                      round(float(stockPrice.replace('$', '')), 2))

        techSector = [
            'AAPL',
            'MSFT',
            'GOOG',
            'AMZN',
            'NVDA',
            'TSLA',
            'META',
            'BABA',
            'CRM',
            'AMD',
            'INTC',
            'PYPL',
            'ATVI',
            'EA',
            'TTD',
            'MTCH',
            'ZG',
            'YELP'
        ]
        realEstate = [
            'PLD',
            'AMT',
            'EQIX',
            'CCI',
            'PSA',
            'SPG-PJ',
            'SPG',
            'O',
            'PSA-PH',
            'PSA-PK',
            'WELL',
            'VICI',
            'CSGP',
            'DLR',
            'SBAC',
            'DLR-PK',
            'BEKE',
            'DLR-PJ',
            'EQR',
            'AVB',
            'EXR',
            'UDR',
            'CBRE',
            'WY',
            'ARE'
        ]
        finance = [
            'JPM',
            'BAC',
            'MS',
            'WFC',
            'RY',
            'GS',
            'SCHW',
            'C',
            'MBFJF',
            'BNPQY',
            'IBN',
            'UBS',
            'BMO',
            'BNS',
            'PNC',
            'ISNPY',
            'TFC'
        ]

        if stockInputField.get() == 's tech':
            scrape_sector_thread = threading.Thread(target=scrape_sector_list, args=(techSector,))
            scrape_sector_thread.start()
        elif stockInputField.get() == 's real estate':
            scrape_sector_thread = threading.Thread(target=scrape_sector_list, args=(realEstate,))
            scrape_sector_thread.start()
        elif stockInputField.get() == 's finance':
            scrape_sector_thread = threading.Thread(target=scrape_sector_list, args=(finance,))
            scrape_sector_thread.start()

    def scrape_stock_info(stockBeingScraped, index):
        def create_graph_button(root):
            buttonGraphPrices = Button(root, text='Graph', command=lambda: showPlot(stockName))
            buttonGraphPrices.grid(row=5 + index, column=5)

        # Adds the stock being scraped from the stock list to the url
        url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')

        # Requests and bs4
        request = requests.get(url)
        result = BeautifulSoup(request.text, 'html.parser')

        try:
            # Find the stock name
            stockName = (result.find('div', {'class': 'zzDege'})).string

        except AttributeError:
            print(stockBeingScraped, url)
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

        create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index)

        theTime = collect_time()
        date = collect_date()

        add_to_db(SearchedBy=SearchedBy[index], name=stockName, priceFloat=round(float(stockPrice.replace('$', '')), 2),
                  date=date, time=theTime, targetPrice=listOfTargetPrices[index])
        create_graph_button(root)

    lock.acquire()

    # Collect stocks from input field
    listOfStocksBeingScraped = stockInputField.get()
    listOfStocksBeingScraped = listOfStocksBeingScraped.split(',')

    # Collect target prices from input field
    listOfTargetPrices = targetPriceInputField.get()
    listOfTargetPrices = listOfTargetPrices.split(',')

    if stockInputField.get() == 's tech' or stockInputField.get() == 's real estate' or stockInputField.get() == 's finance':
        scrape_stock_info_for_sectors(root, stockInputField)

    else:
        for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
            scrape_stock_info_thread = threading.Thread(target=scrape_stock_info, args=(stockBeingScraped, index))
            scrape_stock_info_thread.start()
        lock.release()
