import threading
from sqlite3 import OperationalError
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime
from tkinter import *
from tkinter.ttk import Combobox
import time
from functions.autoRun import autoRun
from functions.plotPrices import showPlot
from functions.upOrDown import fromHigh
from functions.clearEntries import clearEntries
from functions.previousClose import previousClose
from functions.runAll import runAll
from functions.autoRun import stop_autorun

# Connect to the sqlite database
conn = sqlite3.connect('/Users/ab/PycharmProjects/stock-tracker/data-stocks.db')
c = conn.cursor()

# Collects all table names from the sqlite database and creates a tuple
c.execute(f'SELECT tbl_name FROM sqlite_master')
allStocksTuple = c.fetchall()

allStocks = []

# Iterates through the tuple containing all the stock names and adds them to a new list
for COUNT, x in enumerate(allStocksTuple):
    allStocks += x

# Remove watchlist and allstocks tables from the list of stock names so they don't appear in the drop down menu
allStocks.remove('Watchlist')
allStocks.remove('AllStocks')

# Autorunning value set to false so the autorun function doesn't initiate
autorunning = False


def search_it(STOCKS, TARGETPRICE):
    # Scraped stock names are added to this list
    scraped_stock_name = []

    # Scraped stock prices are added to this list
    scraped_stock_price = []

    # User inputs stocks they want to search for, the input is then split
    users_stocks = str(STOCKS.get())
    stocks_split = users_stocks.split(',')
    print('Stocks split', stocks_split)

    # User inputs the target price they hope the stock reaches, the input is then split
    target_price = TARGETPRICE.get()
    target_price = target_price.split(',')
    print('target price', target_price)

    tableNames = []
    
    # Iterates through the list of stock names gathered from the stock input box in the tkinter widget, and finds the table in the sqlite database with the corresponding name
    for index, name in enumerate(scraped_stock_name, 0):
        c.execute(f"SELECT name FROM sqlite_master WHERE Name='{stocks_split[index]}'")
        tableNames += c.fetchone()

    print('stocks split', stocks_split, 'table names', tableNames)

    # Show Button, when clicked will show you the time, price and name of the first stock in your search
    button_show = Button(root, text='Show', command=lambda: show_stocks())
    button_show.configure(activeforeground='red')
    button_show.grid(row=3, column=5, sticky='nsew')

    # Resizes the tkinter widget
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

    # Function is called when 'Show' button is clicked
    def show_stocks():

        # Time title label
        label_time = Label(root, text='Time')
        label_time.configure(foreground='red', font=('Arial', 20))
        label_time.grid(row=3, column=0, sticky='nsew')

        # Stocks title label
        label_all_scraped_stocks = Label(root, text='Stocks')
        label_all_scraped_stocks.configure(foreground='red', font=('Arial', 20))
        label_all_scraped_stocks.grid(row=3, column=1, sticky='nsew')
        
        # Iterates through the list of stock names and creates tkinter labels for them to be added to tkinter widget
        for numberOfStocks, stock in enumerate(scraped_stock_name):
            # Create the stock name label
            label_stock_name = Label(root, text=f'{scraped_stock_name[numberOfStocks]} is at ${scraped_stock_price[numberOfStocks]}')
            label_stock_name.configure(font=('Arial', 16))
            label_stock_name.grid(row=4 + numberOfStocks, column=1, sticky='nsew')

            # Timestamp of when the stock was scraped which will be displayed to the user when the show button is clicked.
            label_current_time = Label(root, text=timestamp)
            label_current_time.configure(font=('Arial', 16))
            label_current_time.grid(row=4 + numberOfStocks, column=0, sticky='nsew')

        # Shows the highest price value for stocks in the tkinter widget
        fromHigh(stocks_split, root)
        
        # Shows the previous closing price in the tkinter widget
        previousClose(users_stocks, root)
        
        # Resizes the tkinter widget
        root.update_idletasks()
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

    # Iterates through the list of stock names to begin webscraping the stock information
    for count, x in enumerate(stocks_split, start=0):
        # New URL with the stock added to it
        url = f'https://www.google.com/finance?q={x}'.replace(' ', '')

        # Requests and scrape the URL
        req = requests.get(url)
        result = BeautifulSoup(req.text, 'html.parser')

        # Find the name of the stock. Use a try/ except statement to see if the stock is listed on Google finance. If not, 'I couldnt find that will be printed to the user' will be printed in the terminal. If an Attribute Error occurs,'I couldnt find that! ' will be printed.
        try:
            name = (result.find('div', {'class': 'zzDege'})).string
            print(url)
            scraped_stock_name += [name]
        except AttributeError:
            print('I couldnt find that!')
            continue

        # Finds the price of the stock and converts it into a float
        price = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
        print(price)
        price_float = float(price[1:])
        scraped_stock_price += [price_float]

        # Timestamp when the data is being logged
        timestamp = str(datetime.now())[11:16]

        # Date of when the data is being logged
        date = str(datetime.now())[:11]

        # Attempts to create the AllStocks table, which stores all web-scraped stock information in it 
        try:
            c.execute('''CREATE TABLE AllStocks
                (
                Name,
                Date,
                Time,
                Price
                )''')
            conn.commit()
        
        # If the table already exists, the below message will be printed in the terminal
        except OperationalError:
            print('Operational Error: Could not create table.')

        # Adds the values to the All Stocks database
        c.execute(f'''INSERT INTO AllStocks VALUES
                (
                "{name}",
                "{date}",
                "{timestamp}",
                "${price_float}"
                )''')
        conn.commit()

        # Use a try/ except statement to test if a table with the same name already exists. If the table exists, the values will be added to the already existing table.
        try:
            # Create table for the stock
            c.execute(f'''CREATE TABLE {x}
                    (
                    Name,
                    Date,    
                    Time,
                    Price
                    )''')

            conn.commit()
        
        # If the table already exists, an error message will be displayed in the terminal
        except OperationalError:
            print('Operational Error: Could not create table.')

        # Adds the values to its corresponding database
        c.execute(f'''INSERT INTO {x} VALUES
                (
                "{name}",
                "{date}",
                "{timestamp}",
                "${price_float}"
                )''')
        conn.commit()

        # 'Finished' will be printed when the values have been added.
        print('finished')
        for num, x in enumerate(stocks_split):
            showPlot(stocks_split[num], root)

        try:
            # If the price of the stock is less than the specified target price, a watchlist table will be created in the database and values will be added
            if price_float <= float(target_price[count]):

                # Creates a table called watchlist if one isnt created already. If an Operational Error occurs, 'Could not create table' will be displayed.
                try:
                    c.execute('''CREATE TABLE Watchlist
                        (
                        Name,
                        Date,
                        Time,
                        Price
                        )''')

                except OperationalError:
                    print('Operational Error: Could not create table.')

                # Adds values to the Watchlist database if the target price is greater than the current price
                c.execute(f'''INSERT INTO Watchlist VALUES
                    (
                    "{name}",
                    "{date}",                    
                    "{timestamp}",
                    "${price_float}"
                    )''')

                conn.commit()

                # Tells the user that the stock was added to the watchlist
                print('Stock added to watchlist')

        # If an operational error occurs, 'Could not insert values into the watchlist' will be displayed
        except OperationalError:
            print('Operational Error: Could not insert values into the watchlist.')
        # If the user didnt include a target price, a message will be displayed in the terminal
        except ValueError:
            print("You didn't include a target price.")

        # URL resets to the original url for the next loop
        url = 'https://www.google.com/finance?q='


# Initiates Tkinter
root = Tk()
root.geometry('365x124')

# Original URL
url = 'https://www.google.com/finance?q='

# Connect to the database and enable the cursor
conn = sqlite3.connect('data-stocks.db')
c = conn.cursor()

# Auto run count
autoRunCount = 0

# 'Stock' Label for the entry widget
label_stock = Label(root, text='Stocks ')
label_stock.configure(font=('Arial', 16))
label_stock.grid(row=1, column=0, sticky='nsew')

# Input the stocks into the Entry widget labeled 'Stocks'
users_stocks = Combobox(root, values=allStocks)
users_stocks.grid(row=1, column=1, columnspan=3, sticky='nsew')

# 'Target price' Label for the entry widget
target_price_label = Label(root, text='Target Price')
target_price_label.configure(font=('Arial', 16))
target_price_label.grid(row=2, column=0, sticky='nsew')

# Input for the price the user wants the stock to reach
target_price = Entry(root)
target_price.grid(row=2, column=1, columnspan=3, sticky='nsew')

# Enter Button, when clicked the inputs will be collected, and separated, then web scraped from 'Google.com/finance' using BeautifulSoup4. The values will then be added to the database.
button_enter = Button(root, text='Enter', command=lambda: search_it(users_stocks, target_price))
button_enter.configure(activeforeground='red')
button_enter.grid(row=1, column=4, sticky='nsew')

# Auto run button
autoRunIt = threading.Thread(target=autoRun, args=(users_stocks, target_price))

button_autoRun = Button(root, text='Auto Run', command=lambda: autoRunIt.start())
button_autoRun.configure(activeforeground='red')
button_autoRun.grid(row=2, column=4, sticky='nsew')

# Auto run stop button
button_autoRun_stop = Button(root, text='Stop', command=lambda: stop_autorun())
button_autoRun_stop.configure(activeforeground='red')
button_autoRun_stop.grid(row=2, column=5, sticky='nsew')

# Clear button
button_clear = Button(root, text='Clear', command=lambda: clearEntries(users_stocks, target_price, root))
button_clear.configure(activeforeground='red')
button_clear.grid(row=1, column=5, sticky='nsew')

# Adds padding between columns
root.columnconfigure(6, pad=30)
root.columnconfigure(7, pad=30)

# Run all button
button_run_all = Button(root, text='Run All', activeforeground='red', command=lambda: runAll(root, conn, c, allStocks))
button_run_all.grid(row=3, column=4, sticky='nsew')

# Resizes the tkinter widget
root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

# Calls the mainloop
root.mainloop()

