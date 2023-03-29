from tkinter import *
import sqlite3
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def showPlot(stock):
    # create a new tkinter root
    newroot = Tk()

    # Connect to db
    conn = sqlite3.connect('new-data-stocks.db')
    c = conn.cursor()

    def get_all_prices():
        def create_title_for_db(name):
            title = name.replace(' ', '')
            title = title.replace('&', '')
            title = title.replace('.', '')
            return title

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

        # Convert prices to floats and add to list named price
        stockPrice = [float(prices[0].replace('$', '')) for prices in AllPrices]

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

    graphData = get_all_prices()
    print(stock)

    get_all_prices()
    plotGraph(graphData[0], graphData[1], graphData[2])
