import sqlite3
from sqlite3 import OperationalError
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *


def showPlot(stock, root):
    def show_graph(fig):
        # create a new tkinter root
        newroot = Tk()
        # Create a canvas widget for the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=newroot)
        canvas.draw()

        # Add the canvas widget to the Tkinter window
        canvas.get_tk_widget().grid(row=1, column=1)
    # Connect to db
    conn = sqlite3.connect('/Users/ab/PycharmProjects/stock-tracker/data-stocks.db')
    c = conn.cursor()

    stocklist = [stock]

    try:
        # Pull all prices from tables
        c.execute(f'SELECT Price FROM {stock} WHERE Price>0')
        AllPrices = c.fetchall()

        # Convert prices to floats and add to list named price
        price = [float(prices[0].replace('$', '')) for prices in AllPrices]

        # Pull all times from the db
        c.execute(f'SELECT Time FROM {stock}')
        AllTimes = c.fetchall()

        priceIndexes = []

        # For prices in list All prices
        for x, y in enumerate(AllPrices):
            # Add indexes of each price to price index list to for x values
            priceIndexes += [x]

        fig, ax = plt.subplots(figsize=(10, 6))

        for COUNT, PRICES in enumerate(price):

            # If the price is equal to the max(price) plot will be magenta
            if PRICES == max(price):
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
                            [price[count], price[count + 1]],
                            c='red')
                # If the currentPrice is less than the next value, the line will be green because there is a positive trend
                elif currentPrice <= AllPrices[count + 1]:
                    ax.plot([priceIndexes[count], priceIndexes[count + 1]],
                            [price[count], price[count + 1]],
                            c='green')

            # If there is an index error, pass
            except IndexError:
                pass

        # Label x and y axis
        ax.set_xlabel('Index', fontsize=15)
        ax.set_ylabel('Price', fontsize=15)

        # Title and show the graph in IDE
        ax.set_title(stock, fontsize=20)
        plt.show()


    except OperationalError:
        pass
