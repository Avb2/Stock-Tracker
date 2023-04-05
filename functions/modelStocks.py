import datetime
from tkinter import *
import sqlite3
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions.databaseQuerying import create_title_for_db, establish_db_connection


def showPlot(stock):
    def get_all_prices(c):
        def convertPriceToFloat(priceString):
            if isinstance(priceString, tuple):
                priceString = priceString[0]

            stockPrice = float(str(priceString).replace('$', ''))
            return stockPrice

        title = create_title_for_db(stock)

        c.execute(f'SELECT SearchedBy FROM {title}')
        searchedByTuple = list(c.fetchall())

        searchedByList = []

        for searchedByValue in searchedByTuple:
            if searchedByValue not in searchedByList:
                searchedByList.append(searchedByValue)
            else:
                pass

        # Pull all prices from tables
        c.execute(f'SELECT Price FROM {title} WHERE Price > -1')
        AllPrices = c.fetchall()

        stockPrice = list(map(convertPriceToFloat, AllPrices))

        priceIndexes = []

        # For prices in list All prices
        for x, y in enumerate(AllPrices):
            # Add indexes of each price to price index list to for x values
            priceIndexes += [x]

        return stockPrice, AllPrices, priceIndexes

    def plotGraph(stockPrice, AllPrices, priceIndexes):
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

    # create a new tkinter root
    newroot = Tk()

    # Connect to db
    c = establish_db_connection()

    graphData = get_all_prices(c[0])
    print(stock)

    get_all_prices(c[0])
    plotGraph(graphData[0], graphData[1], graphData[2])
