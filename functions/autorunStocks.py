import smtplib
import sqlite3
import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
from functions.databaseQuerying import add_to_db


def end_auto_run():
    global autorunValue
    autorunValue = False
    print('Autorun Ended')


def autorun(stockInputField, targetPriceInputField):
    # Connect to sqlite db
    connectionPool = sqlite3.connect('new-data-stocks.db')
    c = connectionPool.cursor()

    # Changes the autorun value to True so the auto run while loop is initiated
    global autorunValue
    autorunValue = True
    print('AutoRun Activated')

    # Collect stocks from input field
    listOfStocksBeingScraped = stockInputField.get()
    listOfStocksBeingScraped = listOfStocksBeingScraped.split(',')

    # Collect target prices from input field
    listOfTargetPrices = targetPriceInputField.get()
    listOfTargetPrices = listOfTargetPrices.split(',')

    # When an email is sent, the stock is added to this list so no more emails will be sent about that particular stock to reduce spamming
    listOfSentEmails = []

    while autorunValue:
        def collect_time():
            # Get timestamp
            time = str(datetime.now())[11:16]
            return time

        def collect_date():
            # Get date
            date = str(datetime.now())[:11]
            return date

        def auto_run_scrape_stock_info(stockBeingScraped, index):
            # Adds the stock being scraped from the stock list to the url
            url = f'https://www.google.com/finance?q={stockBeingScraped}'.replace(' ', '')
            print(url)

            # Requests and bs4
            request = requests.get(url)
            result = BeautifulSoup(request.text, 'html.parser')

            try:
                # Find the stock name
                stockName = (result.find('div', {'class': 'zzDege'})).string

            except AttributeError:
                # If the stock is not found
                print('Name not found on google.com/finance')
                return

            # Find the stock price
            stockPrice = (result.find('div', {'class': 'YMlKec fxKbKc'})).string

            def send_email_if_price_greater_than_tp(listOfSentEmails):

                try:
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


                print(stockName, stockPrice, listOfTargetPrices[index])

            # If the price is below or equal to the target price, and the stock is not on the list of sent emails; an email will be sent to the specified address
            if float(stockPrice.replace('$', '')) <= float(listOfTargetPrices[index]) and stockName not in listOfSentEmails:
                print(float(stockPrice.replace('$', '')), float(listOfTargetPrices[index]))
                send_email_if_price_greater_than_tp(listOfSentEmails)
            
            # Gets time and date
            Date = collect_date()
            Time = collect_time()
            
            # adds the stock information to the database
            add_to_db(SearchedBy=stockBeingScraped, name=stockName, priceFloat=float(stockPrice.replace('$', '')), date=Date,
                      time=Time, targetPrice=0)


            # Sleep for .1 seconds to prevent URL's being printed together in the terminal
            time.sleep(.1)


        for index, stockBeingScraped in enumerate(listOfStocksBeingScraped):
            autoRunThread_scrape = threading.Thread(target=auto_run_scrape_stock_info, args=(stockBeingScraped, index))
            autoRunThread_scrape.start()

        # Waits 10 minutes to scrape again
        time.sleep(600)
