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

    u = []
    for x, y in enumerate(AllPrices):
        u += [x]

    print(u)

    matplotlib.pyplot.scatter(u, price, s=100, c='red')
    matplotlib.pyplot.plot(u, price, c='green')

    matplotlib.pyplot.xlabel('Index', fontsize=15)
    matplotlib.pyplot.ylabel('Price', fontsize=15)
    
    matplotlib.pyplot.title(stock, fontsize=20)
    
    matplotlib.pyplot.show()

