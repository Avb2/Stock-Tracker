import threading
import random
from tkinter import *
from functions.scrapeStock import request_and_parse

# Webscrapes the stock name
def findStockName(result, stockBeingScraped, url):
    try:
        # Find the stock name on google finance
        stockName = (result.find('div', {'class': 'zzDege'})).string
        return stockName
    except AttributeError:
        print(stockBeingScraped, url)
        print('Name not found on google.com/finance')

# Webscrapes the stock price
def findStockPrice(result):
    try:
        # Find the stock price on google finance
        stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
        return stockPrice
    except AttributeError:
        pass


# Selects the list of stocks to be shown
def pickStocksToShow(numberOfStocks):
    popularStocks = [
        'AAPL',
        'MSFT',
        'GOOG',
        'GOOGL',
        'AMZN',
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
    # Selects a specified number of non repeating, random stocks from the popular stocks list to be displayed at the top of tkinter widget
    stocksChosenToShow = list(random.sample(popularStocks, k=numberOfStocks))
    return stocksChosenToShow

# Builds the labels with the stock information
def buildLabels(root, stockInfo, count):
    # Builds a label containing the stock information which is displayed at the top of the tkinter GUI
    label = Label(root, text=stockInfo, foreground='green', bg='black', pady=5, padx=4, font=('Arial, 16'))
    label.grid(row=1, column=count + 1, sticky='nsew')
    # Binds the left mouse click to the label to generate new stocks to be displayed
    label.bind('<Button-1>', lambda event: showPopularStocks(root))


def showPopularStocks(root):
    # Webscrapes the stock information
    def collectStockInfo(stockBeingScraped, count):
        # The URL with the specified stock attached
        url = f"https://www.google.com/finance?q={stockBeingScraped}"

        # Get requests and parse using BeautifulSoup4
        result = request_and_parse(url)

        # Scrapes the stock name
        stockName = findStockName(result, stockBeingScraped, url)

        # Scrapes the stock price
        stockPrice = findStockPrice(result)

        # Creates an f string with the stock name and price to be displayed in the console
        stockInfo = f'{stockName}: {stockPrice}'
        print(stockInfo)

        # Build the labels which are displayed at the top of the tkinter widget
        buildLabels(root, stockInfo, count)

        return stockInfo

    # List of stocks chosen to be displayed
    stocksPicked = pickStocksToShow(numberOfStocks=4)

    # Using threads to simultaneously webscrape the stocks and display them to the user quickly
    for count, stockPicked in enumerate(stocksPicked):
        collectInfoThread = threading.Thread(target=collectStockInfo, args=(stockPicked, count,))
        collectInfoThread.start()
