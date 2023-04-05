import threading
from bs4 import BeautifulSoup
import requests
import random
from tkinter import *


def showPopularStocks(root):
    # Selects the list of stocks to be shown
    def pickStocksToShow(popularStocksList):
        stocksChosenToShow = list(random.sample(popularStocksList, k=5))
        return stocksChosenToShow

    # Webscrapes the stock information
    def collectStockInfo(stockBeingScraped, count):
        def findStockName():
            try:
                # Find the stock name
                stockName = (result.find('div', {'class': 'zzDege'})).string
                return stockName
            except AttributeError:
                print(stockBeingScraped, url)
                print('Name not found on google.com/finance')

        def findStockPrice():
            try:
                # Find the stock price
                stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
                return stockPrice
            except AttributeError:
                pass

        def buildLabels():
            label = Label(root, text=stockInfo, foreground='green', bg='black', pady=5, padx=5,font=('Arial, 16'))
            label.grid(row=1, column=count+1, sticky='nsew')

        url = f"https://www.google.com/finance?q={stockBeingScraped}"

        req = requests.get(url)
        result = BeautifulSoup(req.text, 'html.parser')

        stockName = findStockName()

        stockPrice = findStockPrice()

        stockInfo = f'{stockName}: {stockPrice}'
        print(stockInfo)

        buildLabels()

        return stockInfo

    popularStocks = [
        'AAPL',
        'MSFT',
        'GOOG',
        'GOOGL',
        'AMZN',
        'PCAR',
        'BRKA',
        'BRKB',
        'NVDA',
        'TSLA',
        'META',
        'TSM',
        'V',
        'XOM',
        'UNH',
        'JNJ',
        'WMT',
        'JPM',
        'NVO',
        'PG',
        'MA',
        'LLY',
        'CVX',
        'HD',
        'ABBV',
        'SBGI',
        'CX',
        'JXN',
        'ZIM',
        'ECNCF',
        'GEVO',
        'LCID',
        'MIRM',
        'NNDM',
        'TRMD',
        'VRNA',
        'VTYX',
        'ARDX',
        'OBE',
        'SDRL',
        'PBF',
        'VTNR',
        'PBT'

    ]

    # List of stocks chosen to be displayed
    stocksPicked = pickStocksToShow(popularStocks)

    for count, stockPicked in enumerate(stocksPicked):
        collectInfoThread = threading.Thread(target=collectStockInfo, args=(stockPicked, count,))
        collectInfoThread.start()







