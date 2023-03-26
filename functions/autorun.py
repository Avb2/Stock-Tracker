import time
import smtplib
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def stop_autorun():
    global autorunning
    autorunning = False
    print('Auto run stopped')


def autoRun(STOCKS, TARGETPRICE):
    def sendEmail(stock, emailcount):
        smtp_server = 'smtp.office365.com'
        smtp_port = 587
        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)

        smtp_conn.starttls()
        smtp_conn.login('youremail@outlook.com', 'yourpassword12')

        from_addr = 'hotsauceinmypants@outlook.com'
        to_addr = 'bringuel.alexander@gmail.com'

        email_message = f'Subject: {stock} has hit the target \n\n {stock} has reached your target price of ${target_price[0]} and is currently at {price}. \n\n Date: {date}, Time: {timestamp}, Name: {name}, Price: {price}'
        smtp_conn.sendmail(from_addr, to_addr, email_message)

        print(f'Email sent to {to_addr}')
        smtp_conn.quit()
        emailcount += [1]


    global autorunning
    autorunning = True
    print('Auto Run initiated')

    # User inputs stocks they want to search for, the input is then split
    users_stocks = str(STOCKS.get())
    stocks_split = users_stocks.split(',')

    # User inputs the target price they hope the stock reaches, the input is then split
    target_price = TARGETPRICE.get()
    target_price = target_price.split(',')

    emailcount = []

    while autorunning:
        # Scraped stock names are added to this list
        scraped_stock_name = []

        # Scraped prices are added to this list
        scraped_stock_price = []

        # STOCK INFO
        for count, x in enumerate(stocks_split, start=0):
            # New URL with the stock added to it
            url = f'https://www.google.com/finance?q={x}'

            # Requests and scrape the URL
            req = requests.get(url)
            result = BeautifulSoup(req.text, 'html.parser')

            # Find the name of the stock. Use a try/ except statement to see if the stock is listed on Google finance. If not, 'I couldnt find that will be printed to the user' will be printed. If an Attribute Error occurs,'I couldnt find that!' will be printed.
            try:
                name = (result.find('div', {'class': 'zzDege'})).string
                print(url)
                scraped_stock_name += [name]
            except AttributeError:
                print('I couldnt find that!')

            # Finds the price of the stock and converts it into a float
            price = (result.find('div', {'class': 'YMlKec fxKbKc'})).string
            price_float = float(price[1:])
            scraped_stock_price += [price_float]

            # Timestamp when the data is being logged
            timestamp = str(datetime.now())[11:16]

            # Date of when the data is being logged
            date = str(datetime.now())[:11]

            print(f'Date: {date}, Time: {timestamp}, Name: {name}, Price: {price}')

            if price_float <= int(target_price[0]) and len(emailcount) < 1:
                sendEmail(name, emailcount)

            # URL resets to the original url for the next loop
            url = 'https://www.google.com/finance?q='

            # Sleeps for 10 seconds
            print(autorunning)
            time.sleep(600)
