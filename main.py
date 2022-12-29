from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime

# URL
url = 'https://www.google.com/finance?q='

# Connect to the database and enable the cursor
conn = sqlite3.connect('data-stocks.db')
c = conn.cursor()

# user inputs stocks they want to search for
users_stocks = input('What stock are you looking for?')
stocks_split = users_stocks.split(',')

# Target Price
target_price = input('What is your target price?')
target_price = target_price.split(',')

# Count used to slice target price list
count = 0

# STOCK INFO
for x in stocks_split:
    url = f'{url}{x}'
    req = requests.get(url)
    result = BeautifulSoup(req.text, 'html.parser')

    # Find the name of the stock. Use a try/ except statement to see if the stock is listed on google finance. If not, 'I couldnt find that will be printed to the user.'
    try:
        name = (result.find('div', {'class': 'zzDege'})).string
        print(url)

    except:
        print('I couldnt find that!')
        continue

    # find the price of the stock and convert it into a float
    price = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
    print(price)
    price_float = float(price[1:])

    # Timestamp when the data is being logged
    timestamp = str(datetime.now())[11:16]

    # Date of when the data is being logged
    date = str(datetime.now())[:11]


    try:
        # If the price of the stock is less than the specified target price, a watchlist table will be created in the database and values will be added
        if price_float <= float(target_price[0 + count]):
            # Creates a table called watchlist, if one isnt created already.
            try:
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
                ${price_float}
                ")''')

            conn.commit()

    except:
        pass

        # Use a try/ except statement to test if a table with the same name already exists.If the table exists, the values will be added to the already existing table.
    try:
        # Create table for the stock
        c.execute(f'''CREATE TABLE {x}
            ("
            Name,
            Date,    
            Time,
            Price
            ")''')

        conn.commit()

    except Exception:
            pass

    # Add values to the database
    c.execute(f'''INSERT INTO {x} VALUES
        ("
        {name},
        {date},
        {timestamp},
        ${price_float}
        ")''')

    conn.commit()

    # URL reset
    url = 'https://www.google.com/finance?q='

    # Count increases for the next loop
    count += 1
    print('finished')
