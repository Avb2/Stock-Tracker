from sqlite3 import OperationalError
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from functions.plotPrices import showPlot


def runAll(root, conn, c, allStocks):
    # Official stock names are added to this list
    stocklist = []

    # Scraped prices are added to this list
    pricelist = []

    for stock in allStocks:
        # New URL with the stock added to it
        url = f'https://www.google.com/finance?q={stock}'.replace(' ', '')

        # Requests and scrape the URL
        req = requests.get(url)
        result = BeautifulSoup(req.text, 'html.parser')

        # Find the name of the stock. Use a try/ except statement to see if the stock is listed on Google finance. If not, 'I couldnt find that will be printed to the user' will be printed. If an Attribute Error occurs,'I couldnt find that! ' will be printed.
        try:
            name = (result.find('div', {'class': 'zzDege'})).string
            print(url)
            stocklist += [name]
        except AttributeError:
            print('I couldnt find that!')
            continue

        # Finds the price of the stock and converts it into a float
        price = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
        print(price)
        price_float = float(price[1:])
        pricelist += [price_float]

        # Timestamp when the data is being logged
        timestamp = str(datetime.now())[11:16]

        # Date of when the data is being logged
        date = str(datetime.now())[:11]

        # Adds the values to the database
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
            c.execute(f'''CREATE TABLE {stock}
                               (
                               Name,
                               Date,    
                               Time,
                               Price
                               )''')

            conn.commit()

        except OperationalError:
            print('Operational Error: Could not create table.')

        # Adds the values to the database
        c.execute(f'''INSERT INTO {stock} VALUES
                           (
                           "{name}",
                           "{date}",
                           "{timestamp}",
                           "${price_float}"
                           )''')
        conn.commit()

        # Adds the values to the database
        c.execute(f'''INSERT INTO AllStocks VALUES
                        (
                        "{name}",
                        "{date}",
                        "{timestamp}",
                        "${price_float}"
                        )''')
        conn.commit()

        # 'Finished' will be printed when the values have been added.
        print('finished')

        # URL resets to the original url for the next loop
        url = 'https://www.google.com/finance?q='

    # Creates a matplotlib graph for each stock
    for num, x in enumerate(allStocks):
        showPlot(allStocks[num], root)
