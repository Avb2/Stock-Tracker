import sqlite3
from sqlite3 import OperationalError


def add_to_db(SearchedBy, name, date, time, priceFloat, targetPrice):
    def create_title_for_db(name):
        title = name.replace(' ','')
        title = title.replace('&','')
        title = title.replace('.','')
        print(title)
        return title

    print(name, targetPrice)

    # Connect to sqlite db
    connectionPool = sqlite3.connect('new-data-stocks.db')
    c = connectionPool.cursor()

    # Creates title for db table
    title = create_title_for_db(name)



    # Attempts to create the AllStocks table, which stores all web-scraped stock information in it
    try:
        c.execute('''CREATE TABLE AllStocks
                    (
                    SearchedBy,
                    Name,
                    Date,
                    Time,
                    Price
                    )''')
        connectionPool.commit()

    # If the table already exists, the below message will be printed in the terminal
    except OperationalError:
        print('Operational Error: Could not create table.')

    # Adds the values to the All Stocks database
    c.execute(f'''INSERT INTO AllStocks VALUES
                    (
                    "{(SearchedBy.replace(' ','')).lower}",
                    "{name}",
                    "{date}",
                    "{time}",
                    "${priceFloat}"
                    )''')
    connectionPool.commit()

    # Use a try/ except statement to test if a table with the same name already exists. If the table exists, the values will be added to the already existing table.
    try:
        # Create table for the stock
        c.execute(f'''CREATE TABLE {title}
                        (
                        SearchedBy,
                        Name,
                        Date,    
                        Time,
                        Price
                        )''')

        connectionPool.commit()

    # If the table already exists, an error message will be displayed in the terminal
    except OperationalError:
        print('Operational Error: Could not create table.')

    # Adds the values to its corresponding database
    c.execute(f'''INSERT INTO {title} VALUES
                    (
                    "{(SearchedBy.replace(' ','')).lower}",
                    "{name}",
                    "{date}",
                    "{time}",
                    "${priceFloat}"
                    )''')
    connectionPool.commit()

    # 'Finished' will be printed when the values have been added.
    print('finished')

    try:
        # If the price of the stock is less than the specified target price, a watchlist table will be created in the database and values will be added
        if priceFloat <= float(targetPrice):

            # Creates a table called watchlist if one isnt created already. If an Operational Error occurs, 'Could not create table' will be displayed.
            try:
                c.execute('''CREATE TABLE Watchlist
                    (
                    SearchedBy
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
                "{(SearchedBy.replace(' ','')).lower}",
                "{name}",
                "{date}",                    
                "{time}",
                "${priceFloat}"
                )''')

            connectionPool.commit()

            # Tells the user that the stock was added to the watchlist
            print('Stock added to watchlist')

    # If an operational error occurs, 'Could not insert values into the watchlist' will be displayed
    except OperationalError:
        print('Operational Error: Could not insert values into the watchlist.')
    # If the user didnt include a target price, a message will be displayed in the terminal
    except ValueError:
        print("You didn't include a target price.")

    connectionPool.close()
