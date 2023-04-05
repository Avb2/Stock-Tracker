import sqlite3
from sqlite3 import OperationalError


def create_title_for_db(name):
    if ' ' in name:
        name = name.replace(' ', '')
    if '&' in name:
        name = name.replace('&', '')
    if '.' in name:
        name = name.replace('.', '')
    if ',' in name:
        name = name.replace(',', '')
    if '/' in name:
        name = name.replace('/', '')
    if '(' in name:
        name = name.replace('(', '')
    if ')' in name:
        name = name.replace(')', '')
    title = name
    return title

def establish_db_connection():
    # Connect to sqlite db
    connectionPool = sqlite3.connect('new-data-stocks.db')
    c = connectionPool.cursor()
    return c, connectionPool

def add_to_db(SearchedBy, name, date, time, priceFloat, targetPrice):
    def add_to_all_stocks_db():
        # Attempts to create the AllStocks table, which stores all web-scraped stock information in it
        try:
            c[0].execute('''CREATE TABLE AllStocks
                        (
                        SearchedBy,
                        Name,
                        Date,
                        Time,
                        Price
                        )''')
            c[1].commit()

        # If the table already exists, the below message will be printed in the terminal
        except OperationalError:
            print('Operational Error: Could not create table.')

        # Adds the values to the All Stocks database
        c[0].execute(f'''INSERT INTO AllStocks VALUES
                        (
                        "{SearchedBy.replace(' ', '')}",
                        "{name}",
                        "{date}",
                        "{time}",
                        "${priceFloat}"
                        )''')
        c[1].commit()

    def add_to_specified_stock_db():
        # Use a try/ except statement to test if a table with the same name already exists. If the table exists, the values will be added to the already existing table.
        try:
            # Create table for the stock
            c[0].execute(f'''CREATE TABLE {title}
                            (
                            SearchedBy,
                            Name,
                            Date,    
                            Time,
                            Price
                            )''')

            c[1].commit()

        # If the table already exists, an error message will be displayed in the terminal
        except OperationalError:
            print('Operational Error: Could not create table, it already exists.')

        # Adds the values to its corresponding database
        c[0].execute(f'''INSERT INTO {title} VALUES
                        (
                        "{SearchedBy.replace(' ', '')}",
                        "{name}",
                        "{date}",
                        "{time}",
                        "${priceFloat}"
                        )''')
        c[1].commit()

        # 'Finished' will be printed when the values have been added.
        print('Values have been added to the database')

    def add_to_watchlist_db():
        try:
            # If the price of the stock is less than the specified target price, a watchlist table will be created in the database and values will be added
            if priceFloat <= float(targetPrice):

                # Creates a table called watchlist if one isnt created already. If an Operational Error occurs, 'Could not create table' will be displayed.
                try:
                    c[0].execute('''CREATE TABLE Watchlist
                        (
                        SearchedBy
                        Name,
                        Date,
                        Time,
                        Price
                        )''')

                except OperationalError:
                    print('Operational Error: Could not create Watchlist.')

                # Adds values to the Watchlist database if the target price is greater than the current price
                c[0].execute(f'''INSERT INTO Watchlist VALUES
                    (
                    "{SearchedBy.replace(' ', '')}",
                    "{name}",
                    "{date}",                    
                    "{time}",
                    "${priceFloat}"
                    )''')

                c[1].commit()

                # Tells the user that the stock was added to the watchlist
                print('Stock added to watchlist')

        # If an operational error occurs, 'Could not insert values into the watchlist' will be displayed
        except OperationalError:
            print('Operational Error: Could not insert values into the watchlist.')
        # If the user didnt include a target price, a message will be displayed in the terminal
        except ValueError:
            print("You did not include a target price.")

    c = establish_db_connection()

    # Creates title for db table
    title = create_title_for_db(name)
    print(title)

    add_to_all_stocks_db()

    add_to_specified_stock_db()

    add_to_watchlist_db()

    c[1].close()



def add_to_db_for_sectors(sector, name, date, time, priceFloat):

    def establish_db_connection():
        # Connect to sqlite db
        connectionPool = sqlite3.connect('new-data-stocks.db')
        c = connectionPool.cursor()
        return c, connectionPool
    def add_to_specified_stock_db():
        # Use a try/ except statement to test if a table with the same name already exists. If the table exists, the values will be added to the already existing table.
        try:
            # Create table for the stock
            c[0].execute(f'''CREATE TABLE {sector.replace(' ','')}
                            (
                            Name,
                            Date,    
                            Time,
                            Price
                            )''')

            c[1].commit()

        # If the table already exists, an error message will be displayed in the terminal
        except OperationalError:
            print('Operational Error: Could not create table, it already exists.')

        # Adds the values to its corresponding database
        c[0].execute(f'''INSERT INTO {sector.replace(' ','')} VALUES
                        (
                        "{name}",
                        "{date}",
                        "{time}",
                        "${priceFloat}"
                        )''')
        c[1].commit()

        # 'Finished' will be printed when the values have been added.
        print('Values have been added to the database')


    c = establish_db_connection()
    add_to_specified_stock_db()