import sqlite3
import tkinter
from sqlite3 import OperationalError
import threading
from tkinter import *
from tkinter.ttk import Combobox
from functions.scrapeStock import collect_stock_info
from functions.autorunStocks import autorun
from functions.autorunStocks import end_auto_run
from functions.runAll import run_all_stocks


def get_combobox_values():
    # Connect to sqlite db
    connectionPool = sqlite3.connect('new-data-stocks.db')
    c = connectionPool.cursor()

    # Collects all table names from the sqlite database and creates a tuple
    c.execute(f'SELECT SearchedBy FROM AllStocks')
    allStocksTuple = c.fetchall()

    allStocks = []

    # Adds the value to the drop down box if the value is not already on the list
    for COUNT, x in enumerate(allStocksTuple):
        if x not in allStocks:
            allStocks += [x]

    # Converted tuple to list
    comboboxValuesList = []
    for values in allStocks:
        comboboxValuesList += list(values)

    return comboboxValuesList


def build_page(lock):
    def clear_page(targetPriceInputField, stockInputField):
        targetPriceInputField.grid_forget()
        # Target price input field
        targetPriceInputField = Entry(userInputFrame)
        targetPriceInputField.grid(row=2, column=2)

        stockInputField.grid_forget()
        # Stock input field
        try:
            # Gets values for the combobox drop down
            comboboxValues = get_combobox_values()

            stockInputField = Combobox(userInputFrame, values=comboboxValues)
            stockInputField.grid(row=2, column=1)

        except OperationalError:
            stockInputField = Combobox(userInputFrame)
            stockInputField.grid(row=2, column=1)

    # Value for autorun set to false so autorun doesnt initiate
    autorunValue = False

    # Initialize tkinter widget
    root = Tk()



    ############################# Create frame for headers
    frameHeader = Frame(root)
    frameHeader.grid(row=1, column=1, sticky='nsew')

    # Stock title label
    stockTitleLabel = Label(frameHeader, text='Stocks', foreground='red')
    stockTitleLabel.configure(font=('Arial', 18))
    stockTitleLabel.grid(row=1, column=1, sticky='nsew')

    # Target price title label
    targetPriceTitleLabel = Label(frameHeader, text='Target Price', foreground='red')
    targetPriceTitleLabel.configure(font=('Arial', 18))
    targetPriceTitleLabel.grid(row=2, column=1, sticky='nsew')


    ############################ Create frame for input fields
    userInputFrame = Frame(root)
    userInputFrame.grid(row=1, column=2, sticky='nsew')

    # Stock input field
    try:
        # Gets values for the combobox drop down
        comboboxValues = get_combobox_values()

        stockInputField = Combobox(userInputFrame, values=comboboxValues)
        stockInputField.grid(row=1, column=1)

    except OperationalError:
        stockInputField = Combobox(userInputFrame)
        stockInputField.grid(row=1, column=1)

    # Target price input field
    targetPriceInputField = Entry(userInputFrame)
    targetPriceInputField.grid(row=2, column=1)


    ########################### Create frame for buttons
    frameButtons = Frame(root)
    frameButtons.grid(row=1, column=3, sticky='nsew')

    # Enter Button
    buttonEnter = Button(frameButtons, text='Enter', activeforeground='magenta', font=('Arial', 16),
                         command=lambda: collect_stock_info(root, stockInputField, targetPriceInputField, lock))
    buttonEnter.grid(row=1, column=1, sticky='nsew')

    # Clear Button
    buttonClear = Button(frameButtons, text='Clear', activeforeground='magenta', font=('Arial', 16), command=lambda: clear_page(targetPriceInputField, stockInputField))
    buttonClear.grid(row=1, column=2, sticky='nsew')

    # Run All Button
    buttonRunAll = Button(frameButtons, text='Run All', font=('Arial', 16), command=lambda: run_all_stocks(root, lock))
    buttonRunAll.grid(row=1, column=3, sticky='nsew')

    # Auto Run button
    autorunThread = threading.Thread(target=autorun, args=(stockInputField, targetPriceInputField))

    buttonAutoRun = Button(frameButtons, text='Auto Run', font=('Arial', 16), command=lambda: autorunThread.start())
    buttonAutoRun.grid(row=2, column=1, sticky='nsew')

    # Auto Run End Button
    buttonEndAutoRun = Button(frameButtons, text='End', font=('Arial', 16), command=lambda: end_auto_run())
    buttonEndAutoRun.grid(row=2, column=2, sticky='nsew')



    # Run tkinter root
    root.mainloop()

    # Update widget size whenever new elements are added
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")


