import threading
from tkinter import Label
from functions.scrapeStock import request_and_parse
from functions.universalFunctions import get_stock_name, get_stock_price, pickStocksToShow


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
        stockName = get_stock_name(result)

        # Scrapes the stock price
        stockPrice = get_stock_price(result)

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
