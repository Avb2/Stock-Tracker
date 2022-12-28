from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime

# Connect to the database and enable the cursor
conn = sqlite3.connect('data-stocks.db')
c = conn.cursor()

# Take the stocks the user wants to search for and add them to the url
users_stocks = [input('What stock are you looking for?')]
url = 'https://www.google.com/finance?q='

# Target Price

target_price = float(input('What is your target price?'))

# Loop begins, iterates through each stock and finds data off google finance. Then creates table with values for the stock information.
for stock in users_stocks:
    url += stock

    # Send requests to google finance
    req = requests.get(url)

    # Parse the URL with Beautiful Soup
    result = BeautifulSoup(req.text, 'html.parser')

    # Find the name of the stock. Use a try/ except statement to see if the stock is listed on google finance. If not, 'I couldnt find that will be printed to the user.'
    try:
        name = result.find('div', {'class': 'zzDege'})
        name = name.string
        print(name)
        print(url)

    except Exception:
        print('I couldnt find that.')

    # Find the Price of the stock.
    price = result.find('div', {'class': 'YMlKec fxKbKc'})
    price = price.string
    print(price)
    pr = float(price[1:])

    # Timestamp when the data is being logged.
    timestamp = str(datetime.now())[11:16]

    # Date of when the data is being logged.
    date = str(datetime.now())[:11]

    # Use a try/ except statement to test if a table with the same name already exists.If the table exists, the values will be added to the already existing table.
    try:
        # Create table for the stock
        c.execute(f'''CREATE TABLE {stock}
        ("
        Name,
        Date,
        Time,
        Price
        ")''')

        conn.commit()

    # If the table already exists, values will be inserted into the table.
    except Exception:
        pass

    # Add values to the database
    c.execute(f'''INSERT INTO {stock} VALUES
            ("
            {name},
            {date},
            {timestamp},
            ${pr}
            ")''')

    conn.commit()

    # if the price is below the target price, a new table called WatchList will be created.
    if pr <= target_price:
        try:
            # Create table for the stock
            c.execute('''CREATE TABLE Watchlist
            ("
            Name,
            Date,
            Time,
            Price
            ")''')


        except:
            pass

        # Add values to the database
        c.execute(f'''INSERT INTO Watchlist VALUES
            ("
            {name},
            {date},
            {timestamp},
            ${pr}
            ")''')

        conn.commit()

    # URL Reset at end of loop
    url = 'https://www.google.com/finance?q='
