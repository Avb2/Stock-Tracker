import requests
from bs4 import BeautifulSoup
from tkinter import *


def previousClose(stocks, root):
    label_previous_close_title = Label(root, text='Previous Close', foreground='red', font=('Arial', 20))
    label_previous_close_title.grid(row=3, column=7, sticky='nsew')

    stocks = [stocks.get()]

    for count, x in enumerate(stocks, start=0):
        # New URL with the stock added to it
        url = f'https://www.google.com/finance?q={x}'.replace(' ', '')

        print(url)
        # Requests and scrape the URL
        req = requests.get(url)
        result = BeautifulSoup(req.text, 'html.parser')

        # Find the name of the stock. Use a try/ except statement to see if the stock is listed on Google finance. If not, 'I couldnt find that will be printed to the user' will be printed. If an Attribute Error occurs,'I couldnt find that! ' will be printed.
        try:
            previousDayClose = result.find('div', {'class': 'P6K39c'}).string
            print('PDC', previousDayClose)

            name = result.find('div', {'class': 'zzDege'}).string

        except AttributeError:
            print('I couldnt find that!')
            continue

        label_previous_close = Label(root, text=f'{name}: {previousDayClose}', font=('Arial', 16), borderwidth=2,
                                     highlightcolor='red', relief='solid')
        label_previous_close.grid(row=count + 4, column=7, sticky='nsew')

    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
