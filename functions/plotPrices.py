import matplotlib
from matplotlib import pyplot
import sqlite3
from sqlite3 import OperationalError


def showPlot(stock):
    conn = sqlite3.connect('/Users/ab/PycharmProjects/stock-tracker/data-stocks.db')
    c = conn.cursor()

    try:
        c.execute(f'SELECT Price FROM {stock} WHERE Price>0')
        AllPrices = c.fetchall()

        price = [float(prices[0].replace('$', '')) for prices in AllPrices]
        print(price)

        c.execute(f'SELECT Time FROM {stock}')
        AllTimes = c.fetchall()

        priceIndexes = []
        for x, y in enumerate(AllPrices):
            priceIndexes += [x]

        for COUNT, PRICES in enumerate(price):
            if PRICES == max(price):
                print('match')
                maxPIndex = COUNT
                matplotlib.pyplot.scatter(maxPIndex, PRICES, s=70, c='magenta')
            else:
                allPricesIndexes = COUNT
                matplotlib.pyplot.scatter(allPricesIndexes, PRICES, s=50, c='blue')

        for count, currentPrice in enumerate(AllPrices, 0):
            try:
                if count == len(AllPrices):
                    break

                elif currentPrice > AllPrices[count + 1]:
                    matplotlib.pyplot.plot([priceIndexes[count], priceIndexes[count + 1]],
                                           [price[count], price[count + 1]],
                                           c='red')

                elif currentPrice <= AllPrices[count + 1]:
                    matplotlib.pyplot.plot([priceIndexes[count], priceIndexes[count + 1]],
                                           [price[count], price[count + 1]],
                                           c='green')
            except IndexError:
                pass

        matplotlib.pyplot.xlabel('Index', fontsize=15)
        matplotlib.pyplot.ylabel('Price', fontsize=15)

        matplotlib.pyplot.title(stock, fontsize=20)
        matplotlib.pyplot.show()

    except OperationalError:
        pass
