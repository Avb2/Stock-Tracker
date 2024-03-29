import threading
from tkinter import Label
from functions.databaseQuerying import add_to_db
from functions.databaseQuerying import add_to_db_for_sectors
from functions.modelStocks import showPlot
from functions.universalFunctions import collect_time, collect_date, request_and_parse, get_stock_name, get_stock_price, \
    change_searchedBy_to_lower, collect_and_split_stock, collect_and_split_target_price, establish_db_connection


def create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index):
    # Get the time and date
    time = collect_time()
    date = collect_date()

    # Time/ Date Title label
    timeDateTitleLabel = Label(root, text='Date/Time', borderwidth=1.5, relief='solid', font=('Arial', 21), padx=100)
    timeDateTitleLabel.grid(row=1, column=1, columnspan=20, sticky='nsew')

    # Stock Title label
    stockTitleLabel = Label(root, text='Name', borderwidth=1.5, relief='solid', font=('Arial', 21), padx=100)
    stockTitleLabel.grid(row=1, column=22, columnspan=20, sticky='nsew')

    # Price Title label
    priceTitleLabel = Label(root, text='Price', borderwidth=1.5, relief='solid', font=('Arial', 21), padx=100)
    priceTitleLabel.grid(row=1, column=43, columnspan=20, sticky='nsew')

    # Closing price Title label
    closingPriceTitleLabel = Label(root, text='Closing Price', borderwidth=1.5, relief='solid',
                                   font=('Arial', 21), padx=100)
    closingPriceTitleLabel.grid(row=1, column=64, sticky='nsew')

    # Displays current time/date
    currentTimeDateLabel = Label(root, text=f'{date} : {time}', font=('Arial', 21), bg='black', foreground='green')
    currentTimeDateLabel.grid(row=2 + index, column=1, columnspan=20, sticky='nsew')

    # Displays stock name
    stockNameLabel = Label(root, text=f'{stockName}: ', font=('Arial', 21), bg='black', foreground='green')
    stockNameLabel.grid(row=2 + index, column=22, columnspan=20, sticky='nsew')
    stockNameLabel.bind('<Button-1>', lambda event: showPlot(stockName))

    # Displays stock price
    stockPriceLabel = Label(root, text=stockPrice, font=('Arial', 21), bg='black', foreground='green')
    stockPriceLabel.grid(row=2 + index, column=43, columnspan=20, sticky='nsew')

    # Displays Previous closing price
    stockPreviousClosingPriceLabel = Label(root, text=stockPreviousClosingPrice, font=('Arial', 21), bg='black',
                                           foreground='green')
    stockPreviousClosingPriceLabel.grid(row=2 + index, column=64, sticky='nsew')

    # Adds padding between all rows of stock information
    for num in range(index):
        root.rowconfigure(num, pad=10)


def collect_stock_info(root, stockInputField, targetPriceInputField, lock):
    def scrape_stock_info(stockBeingScraped, index):
        # Adds the stock being scraped from the stock list to the url
        url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')

        # Requests and bs4
        result = request_and_parse(url)

        # Find the stock name
        stockName = get_stock_name(result)

        # Find the stock price
        stockPrice = get_stock_price(result)

        print(stockName, stockPrice)

        SearchedByNames = []

        # Converts the SearchedBy value to lowercase for uniformity
        SearchedBy = change_searchedBy_to_lower(listOfStocksBeingScraped, SearchedByNames)

        try:
            # Find the previous closing price
            stockPreviousClosingPrice = result.find('div', {'class': 'P6K39c'}).string

            # Create labels for the stock information
            create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index)

        except AttributeError:
            pass



        # Get the time and date
        theTime = collect_time()
        date = collect_date()

        try:
            # Add the values to the specified database table in the new-data-stocks.db file
            add_to_db(SearchedBy=SearchedBy[index], name=stockName, priceFloat=round(float(stockPrice.replace('$', '')), 2),
                      date=date, time=theTime, targetPrice=listOfTargetPrices[index])
        except IndexError:
            add_to_db(SearchedBy='GroupStock', name=stockName, priceFloat=round(float(stockPrice.replace('$', '')), 2),
                      date=date, time=theTime, targetPrice=0)

    def scrape_stock_info_for_sectors(root, stockInputField):
        def scrape_sector_list(sector):
            for index, stockBeingScraped in enumerate(sector):
                # Adds the stock being scraped from the stock list to the url
                url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')

                # Send requests and beautiful soup
                result = request_and_parse(url)

                try:
                    # Find the stock name
                    stockName = (result.find('div', {'class': 'zzDege'})).string

                except AttributeError:
                    # If the stock name cannot be found, the name of the stock and the url will be displayed in the
                    # console with a 'Name Not Found' message and will iterate to the next stock
                    print(stockBeingScraped, url)
                    print(f'{stockBeingScraped} not found on google.com/finance')
                    continue

                # Find the stock price
                stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string

                # Displays the name and price in the console
                print(stockName, stockPrice)

                SearchedBy = []

                # Find the previous closing price
                stockPreviousClosingPrice = result.find('div', {'class': 'P6K39c'}).string

                # Creates labels for the stocks that were scraped
                create_stock_info_labels(root, stockName, stockPrice, stockPreviousClosingPrice, index)

                # Gets the current time and date
                theTime = collect_time()
                date = collect_date()

                # Adds the information to the specified sector's table in the database file
                add_to_db_for_sectors(stockInputField.get(), stockName, date, theTime,
                                      round(float(stockPrice.replace('$', '')), 2))

                # Adds the information to the stock information table
                add_to_db(SearchedBy=stockName.lower(), name=stockName, date=date, time=theTime, priceFloat=round(float(stockPrice.replace('$', '')), 2), targetPrice=0)

        # List of stocks for searching by sectors
        techSector = [
            'AAPL',
            'MSFT',
            'GOOG',
            'AMZN',
            'NVDA',
            'TSLA',
            'META',
            'BABA',
            'CRM',
            'AMD',
            'INTC',
            'PYPL',
            'ATVI',
            'EA',
            'TTD',
            'MTCH',
            'ZG',
            'YELP'
        ]
        realEstate = [
            'PLD',
            'AMT',
            'EQIX',
            'CCI',
            'PSA',
            'SPG-PJ',
            'SPG',
            'O',
            'PSA-PH',
            'PSA-PK',
            'WELL',
            'VICI',
            'CSGP',
            'DLR',
            'SBAC',
            'DLR-PK',
            'BEKE',
            'DLR-PJ',
            'EQR',
            'AVB',
            'EXR',
            'UDR',
            'CBRE',
            'WY',
            'ARE'
        ]
        finance = [
            'JPM',
            'BAC',
            'MS',
            'WFC',
            'RY',
            'GS',
            'SCHW',
            'C',
            'MBFJF',
            'BNPQY',
            'UBS',
            'BMO',
            'BNS',
            'PNC',
            'TFC'
        ]

        # If the user inputs "s tech" it will scrape the tech sector list of stocks
        if stockInputField.get() == 's tech':
            scrape_sector_thread = threading.Thread(target=scrape_sector_list, args=(techSector,))
            scrape_sector_thread.start()

        # If the user inputs "s real estate" it will scrape the real estate sector list of stocks
        elif stockInputField.get() == 's real estate':
            scrape_sector_thread = threading.Thread(target=scrape_sector_list, args=(realEstate,))
            scrape_sector_thread.start()

        # If the user inputs "s finance" it will scrape the finance sector list of stocks
        elif stockInputField.get() == 's finance':
            scrape_sector_thread = threading.Thread(target=scrape_sector_list, args=(finance,))
            scrape_sector_thread.start()

    lock.acquire()

    # Collect stocks from input field
    listOfStocksBeingScraped = collect_and_split_stock(stockInputField)

    # Collect target prices from input field
    listOfTargetPrices = collect_and_split_target_price(targetPriceInputField)

    # Connect to sqlite db
    c = establish_db_connection()

    # Collects the groupNames from the AllGroups table in the new-data-stocks database table
    c[0].execute('SELECT name FROM sqlite_master WHERE type="table"')
    allTableNames = c[0].fetchall()
    # Converts from tuple to list
    allTableNames = [x[0] for x in allTableNames]

    print(allTableNames)

    for tableName in allTableNames:
        if tableName == listOfStocksBeingScraped[0]:
            print(tableName, listOfStocksBeingScraped[0])

            # Collects the names from the table names and converts them into a list
            c[0].execute(f'SELECT Name FROM {tableName}')
            stocksInTable = c[0].fetchall()
            stocksInTable = [stock[0] for stock in stocksInTable]

            # Creates a thread and scrapes the stock information
            for index, stockInTable in enumerate(stocksInTable):
                scrape_stock_info_thread = threading.Thread(target=scrape_stock_info, args=(stockInTable, index))
                scrape_stock_info_thread.start()

# If the user searches by sectors using the s keywords, the scrape stock by sectors function will be called
    if stockInputField.get() == 's tech' or stockInputField.get() == 's real estate' or stockInputField.get() == 's finance':
        scrape_stock_info_for_sectors(root, stockInputField)

    else:
        # Creates a thread for each stock in the list so all stocks are scraped at the same time
        for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
            scrape_stock_info_thread = threading.Thread(target=scrape_stock_info, args=(stockBeingScraped, index))
            scrape_stock_info_thread.start()

            lock.release()
