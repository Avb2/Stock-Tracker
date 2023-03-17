import matplotlib
from matplotlib import pyplot
import sqlite3


def showPlot(stock):
    conn = sqlite3.connect('data-stocks.db')
    c = conn.cursor()

    c.execute(f'SELECT Price FROM {stock} WHERE Price>0')
    AllPrices = c.fetchall()

    price = [float(prices[0].replace('$', '')) for prices in AllPrices]
    print(price)

    c.execute(f'SELECT Time FROM {stock}')
    AllTimes = c.fetchall()

    priceIndexes = []
    for x, y in enumerate(AllPrices):
        priceIndexes += [x]

    matplotlib.pyplot.scatter(priceIndexes, price, s=50, c='blue')

    for count, currentPrice in enumerate(AllPrices, 0):
        try:
            if count == len(AllPrices):
                break

            elif currentPrice > AllPrices[count + 1]:
                matplotlib.pyplot.plot([priceIndexes[count], priceIndexes[count + 1]], [price[count], price[count + 1]],
                                       c='red')

            elif currentPrice <= AllPrices[count + 1]:
                matplotlib.pyplot.plot([priceIndexes[count], priceIndexes[count + 1]], [price[count], price[count + 1]],
                                       c='green')
        except IndexError:
            pass

    matplotlib.pyplot.xlabel('Index', fontsize=15)
    matplotlib.pyplot.ylabel('Price', fontsize=15)

    matplotlib.pyplot.title(stock, fontsize=20)
    matplotlib.pyplot.show()

