import sqlite3
from datetime import datetime
import random
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Get the current time and format it using the datetime package
def collect_time():
    # Get timestamp using datetime package
    time = str(datetime.now())[11:16]
    return time


# Get the current date and format it using the datetime package
def collect_date():
    # Get date using datetime package
    date = str(datetime.now())[:11]
    return date


# Webscrape the stock name from google finance
def get_stock_name(result):
    try:
        # Find the stock name
        stockName = (result.find('div', {'class': 'zzDege'})).string
        return stockName

    except AttributeError:
        # If the stock name cannot be found, the name of the stock and the url will be displayed in the
        # console with a 'Name Not Found' message and will iterate to the next stock
        # If the stock is not found
        print('Name not found on google.com/finance')
        return


# Webscrape the stock price from google finance
def get_stock_price(result):
    try:
        stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
        return stockPrice
    except AttributeError:
        return


# Get the stock names from the stock input field and split it into a list
def collect_and_split_stock(stockInputField):
    # Collect stocks from input field
    listOfStocksBeingScraped = stockInputField.get()
    listOfStocksBeingScraped = listOfStocksBeingScraped.split(',')

    return listOfStocksBeingScraped


# Get the target price from the target price input field and split it into a list
def collect_and_split_target_price(targetPriceInputField):
    # Collect target prices from input field
    listOfTargetPrices = targetPriceInputField.get()
    listOfTargetPrices = listOfTargetPrices.split(',')

    return listOfTargetPrices


# Create a title that is insertable into sqlite by removing bad characters
def create_title_for_db(name):
    badCharacters = [' ', '&', '.', ',', '/', '(', ')', '-']

    for badCharacter in badCharacters:
        if badCharacter in name:
            name = name.replace(badCharacter, '')

    title = name
    return title


# Establish a connection to the new-data-stocks.db database file
def establish_db_connection():
    # Connect to sqlite db
    connectionPool = sqlite3.connect('new-data-stocks.db')
    c = connectionPool.cursor()
    return c, connectionPool


# Converts the scraped string of a price to a float and replace the dollar sign with ''
def convertPriceToFloat(priceString):
    if isinstance(priceString, tuple):
        priceString = priceString[0]

    stockPrice = float(str(priceString).replace('$', ''))
    return stockPrice


# Collects all the prices from the specified stocks database table and returns them to the user
def get_all_prices(c, stock):
    # Creates a title that will work in sqlite3 (meaning no bad characters)
    title = create_title_for_db(stock)

    # Gets the SearchedBy value from the database table for the stock named after the title
    c.execute(f'SELECT SearchedBy FROM {title}')
    searchedByTuple = list(c.fetchall())

    # List that the searchByValues are added to so that it is mutable
    searchedByList = []

    # for each value in the SearchedByTuple, if the value is not in the searchedByList, it will be added to the list.
    for searchedByValue in searchedByTuple:
        if searchedByValue not in searchedByList:
            searchedByList.append(searchedByValue)
        else:
            pass

    # Pull all prices from tables
    c.execute(f'SELECT Price FROM {title} WHERE Price > -1')
    AllPrices = c.fetchall()

    # Converts each value in the AllPrices tuple to a float, and creates a list
    stockPrice = list(map(convertPriceToFloat, AllPrices))

    priceIndexes = []

    # For prices in list All prices
    for x, y in enumerate(AllPrices):
        # Add indexes of each price to price index list to for x values
        priceIndexes += [x]

    return stockPrice, AllPrices, priceIndexes


# Creates the graph for the stock price data and creates a new root in which the graph is displayed to the user
def plotGraph(newroot, stock, stockPrice, AllPrices, priceIndexes):
    fig, ax = plt.subplots(figsize=(10, 6))

    for COUNT, PRICES in enumerate(stockPrice):

        # If the price is equal to the max(price) plot will be magenta
        if PRICES == max(stockPrice):
            maxPIndex = COUNT
            ax.scatter(maxPIndex, PRICES, s=70, c='magenta')
        else:
            # if the value is just a normal price, plot will be blue
            allPricesIndexes = COUNT
            ax.scatter(allPricesIndexes, PRICES, s=50, c='blue')

    # For the current price in AllPrices
    for count, currentPrice in enumerate(AllPrices, 0):
        try:
            # If the count reach == length(AllPrices), the loop will break
            if count == len(AllPrices):
                break

            # If the current price is greater than the next value, the line will be red because there is a negative trend
            elif currentPrice > AllPrices[count + 1]:
                ax.plot([priceIndexes[count], priceIndexes[count + 1]],
                        [stockPrice[count], stockPrice[count + 1]],
                        c='red')
            # If the currentPrice is less than the next value, the line will be green because there is a positive trend
            elif currentPrice <= AllPrices[count + 1]:
                ax.plot([priceIndexes[count], priceIndexes[count + 1]],
                        [stockPrice[count], stockPrice[count + 1]],
                        c='green')
        # If there is an index error, pass
        except IndexError:
            pass
    # Label x and y axis
    ax.set_xlabel('Index', fontsize=15)
    ax.set_ylabel('Price', fontsize=15)

    # Title and show the graph in IDE
    ax.set_title(stock, fontsize=20)

    # Create a canvas widget for the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=newroot)
    canvas.draw()

    # Add the canvas widget to the Tkinter window
    canvas.get_tk_widget().grid(row=1, column=1)


# Collects values from the database table 'AllStocks', removes any repeating values, then applies the values to the tkinter drop down menu (combo box)
def get_combobox_values():
    # Connect to sqlite db
    c = establish_db_connection()

    # Collects all table names from the sqlite database and creates a tuple
    c[0].execute(f'SELECT SearchedBy FROM AllStocks')
    allStocksTuple = c[0].fetchall()

    c[0].execute(f'SELECT GroupName FROM AllGroups')
    allGroupsTuple = c[0].fetchall()

    allStocks = []

    # Adds the value to the drop down box if the value is not already on the list
    for x in allStocksTuple:
        if x not in allStocks:
            allStocks += [x]

    for y in allGroupsTuple:
        if y not in allStocks:
            allStocks += [y]

    return allStocks


# Get requests and parse with requests and bs4 packages
def request_and_parse(url):
    # Requests and bs4
    request = requests.get(url)
    result = BeautifulSoup(request.text, 'html.parser')
    return result


# Changes the user's search by value, that is collected from the stock input field, to lower case for uniformity
def change_searchedBy_to_lower(listOfStocksBeingScraped, SearchedByNames):
    # What the user searched the stock by
    for theStock in listOfStocksBeingScraped:
        SearchedByNames += [theStock.lower()]
    return SearchedByNames


# Selects the random list of stocks to be shown at the top of the tkinter widget
def pickStocksToShow(numberOfStocks):
    popularStocks = [
        'AAC',
        'AAL',
        'AAON',
        'AAPL',
        'AAT',
        'AB',
        'ABB',
        'ABBV',
        'ABCB',
        'ABCM',
        'ABNB',
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


