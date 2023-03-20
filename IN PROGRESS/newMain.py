from sqlite3 import OperationalError
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime
from tkinter import *
import time
from functions.autoRun import autoRun
from functions.autoRun import stop_autorun
from functions.plotPrices import showPlot


def scrape_stock(stockNameInput, targetPriceInput):
    def getTimeDate():
        # Timestamp when the data is being logged
        timestamp = str(datetime.now())[11:16]

        # Date of when the data is being logged
        date = str(datetime.now())[:11]

        dateAndTime = {'Date': date, 'Time': timestamp}
        return dateAndTime

    officialStockName = []

    scraped_stock_prices = []

    stockName = str(stockNameInput.get())
    stockName = stockName.split(',')

    targetPrice = str(targetPriceInput.get())
    targetPrice = targetPrice.split(',')

    for count, x in enumerate(stockName, start=0):
        # New URL with the stock added to it
        url = f'https://www.google.com/finance?q={x}'

        # Requests and scrape the URL
        req = requests.get(url)
        result = BeautifulSoup(req.text, 'html.parser')

        # Find the name of the stock. Use a try/ except statement to see if the stock is listed on Google finance. If not, 'I couldnt find that will be printed to the user' will be printed. If an Attribute Error occurs,'I couldnt find that! ' will be printed.
        try:
            name = (result.find('div', {'class': 'zzDege'})).string
            print(url)
            officialStockName += [name]

        except AttributeError:
            print('I couldnt find that!')
            continue

        # Finds the price of the stock and converts it into a float
        price = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
        print(price)
        price_float = float(price[1:])
        scraped_stock_prices += [price_float]

        timeDate = getTimeDate()

        for stockNames, stockPrice in zip(stockName, scraped_stock_prices):
            info = {'Time and Date': timeDate, 'Stock Name': officialStockName, 'Stock Price': stockPrice}

        print(info)


    def showStocks():
        for numberOfStocks, stock in enumerate(stockName):
            # Create the stock name label
            label_stock_name = Label(root,
                                     text=f'{officialStockName[numberOfStocks]} is at ${scraped_stock_prices[numberOfStocks]}')
            label_stock_name.grid(row=3 + numberOfStocks, column=1, sticky='nsew')

            # Timestamp of when the stock was scraped which will be displayed to the user when the show button is clicked.
            label_current_time = Label(root, text=timeDate)
            label_current_time.grid(row=3 + numberOfStocks, column=0, sticky='nsew')

            # Timestamp of when the stock was scraped which will be displayed to the user when the show button is clicked.
            bb = Button(root, text='DB', highlightcolor='red')
            bb.grid(row=3 + numberOfStocks, column=4, sticky='nsew')

            root.update_idletasks()
            root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")


        return showStocks()

    showStocks = showStocks()




# Initiates Tkinter
root = Tk()
root.geometry('365x124')

# Original URL
url = 'https://www.google.com/finance?q='

# Connect to the database and enable the cursor
conn = sqlite3.connect('data-stocks.db')
c = conn.cursor()

# 'Stock' Label for the entry widget
label_stock = Label(root, text='Stocks ')
label_stock.grid(row=1, column=0, sticky='nsew')

# Input the stocks into the Entry widget labeled 'Stocks'
users_stocks = Entry(root)
users_stocks.grid(row=1, column=1, columnspan=3, sticky='nsew')

# 'Target price' Label for the entry widget
target_price_label = Label(root, text='Target Price')
target_price_label.grid(row=2, column=0, sticky='nsew')

# Input for the price the user wants the stock to reach
target_price = Entry(root)
target_price.grid(row=2, column=1, columnspan=3, sticky='nsew')

# Enter Button, when clicked the inputs will be collected, and separated, then web scraped from 'Google.com/finance' using BeautifulSoup4. The values will then be added to the database.
button_enter = Button(root, text='Enter', command=lambda: scrape_stock(users_stocks, target_price))
button_enter.grid(row=1, column=5, sticky='nsew')

# Auto run button
button_autoRun = Button(root, text='Auto Run')
button_autoRun.grid(row=2, column=5, sticky='nsew')

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

# Calls the mainloop
root.mainloop()
