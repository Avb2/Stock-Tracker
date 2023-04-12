import smtplib
import threading
import time
from functions.databaseQuerying import add_to_db
from functions.databaseQuerying import establish_db_connection
from functions.scrapeStock import request_and_parse
from functions.universalFunctions import collect_time, collect_date, get_stock_name, get_stock_price, \
    collect_and_split_stock, collect_and_split_target_price
from functions.settings import open_settings


def end_auto_run():
    global autorunValue
    # The autorunvalue is set to false to end the auto run function
    autorunValue = False
    print('Autorun Ended')


def autorun(stockInputField, targetPriceInputField):
    def auto_run_scrape_stock_info(stockBeingScraped, index):
        def send_email_if_price_greater_than_tp(listOfSentEmails):

            try:
                # Get time and date
                time = collect_time()
                date = collect_date()

                # Connects to the smtp server
                smtp_server = 'smtp.office365.com'
                smtp_port = 587
                smtp_conn = smtplib.SMTP(smtp_server, smtp_port)

                # Login to the outlook email address the emails will be sent from
                smtp_conn.starttls()
                smtp_conn.login('yourEmail@outlook.com', 'yourPassword')

                # Fill in the send/recieve addresses
                from_addr = 'stocktrackerpythonscript@outlook.com'
                to_addr = 'bringuel.alexander@gmail.com'

                # Email content
                email_message = f'Subject: {stockName} has hit the target \n\n {stockName} has reached your target price of ${listOfTargetPrices[index]} and is currently at {stockPrice}. \n\n Date: {date}, Time: {time}, Name: {stockName}, Price: {stockPrice}'

                # Send the email
                smtp_conn.sendmail(from_addr, to_addr, email_message)

                # Print in terminal that an email has been sent to inform the user
                print(f'Email sent to {to_addr}')

                # Close the connection the smtp server
                smtp_conn.quit()

                # Adds the sent email to the list of sent emails so it wont send anymore about that stock
                listOfSentEmails += [stockName]

            except TypeError:
                print(TypeError)

            # Displays stock name, price, and target price in the console
            print(stockName, stockPrice, listOfTargetPrices[index])

        # Adds the stock being scraped from the stock list to the url
        url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')
        print(url)

        # Requests and bs4
        result = request_and_parse(url)

        # Finds the stock name
        stockName = get_stock_name(result)

        # Find the stock price
        stockPrice = get_stock_price(result)

        try:
            # If the price is below or equal to the target price, and the stock is not on the list of sent emails; an email will be sent to the specified address
            if float(stockPrice.replace('$', '')) <= float(listOfTargetPrices[index]) and stockName not in listOfSentEmails:
                print(float(stockPrice.replace('$', '')), float(listOfTargetPrices[index]))
                send_email_if_price_greater_than_tp(listOfSentEmails)
        except AttributeError:
            return

        # Gets time and date
        Date = collect_date()
        Time = collect_time()

        # Adds the stock information to the database
        add_to_db(SearchedBy=stockBeingScraped, name=stockName, priceFloat=float(stockPrice.replace('$', '')),
                  date=Date,
                  time=Time, targetPrice=0)

        # Sleep for .1 seconds to prevent URL's being printed together in the terminal
        time.sleep(.1)

    # Connect to the database
    establish_db_connection()

    # Changes the autorun value to True so the auto run while loop is initiated
    global autorunValue
    autorunValue = True
    print('AutoRun Activated')

    # Collect stocks from input field
    listOfStocksBeingScraped = collect_and_split_stock(stockInputField)

    # Collect target prices from input field
    listOfTargetPrices = collect_and_split_target_price(targetPriceInputField)

    # When an email is sent, the stock is added to this list so no more emails will be sent about that particular stock to reduce spamming
    listOfSentEmails = []

    while autorunValue:
        # While autorun is active, threads will be created to webscrape the stocks simultaneously using the auto_run_scrape_stock_info function
        for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
            autoRunThread_scrape = threading.Thread(target=auto_run_scrape_stock_info, args=(stockBeingScraped, index))
            autoRunThread_scrape.start()

        # Waits 10 minutes to scrape again
        time.sleep(600)
