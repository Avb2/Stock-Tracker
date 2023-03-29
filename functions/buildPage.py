import sqlite3
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
        targetPriceInputField = Entry(root)
        targetPriceInputField.grid(row=2, column=2)

        stockInputField.grid_forget()
        # Stock input field
        try:
            # Gets values for the combobox drop down
            comboboxValues = get_combobox_values()

            stockInputField = Combobox(root, values=comboboxValues)
            stockInputField.grid(row=2, column=1)

        except OperationalError:
            stockInputField = Combobox(root)
            stockInputField.grid(row=2, column=1)


    comboboxValues = get_combobox_values()

    # Value for autorun set to false so autorun doesnt initiate
    autorunValue = False

    # Initialize tkinter widget
    root = Tk()

    # Adding padding between labels
    root.columnconfigure(1, pad=8)
    root.columnconfigure(2, pad=8)
    root.columnconfigure(3, pad=8)
    root.columnconfigure(4, pad=8)
    root.rowconfigure(2, pad=15)

    # Stock title label
    stockTitleLabel = Label(root, text='Stocks', foreground='red')
    stockTitleLabel.configure(font=('Arial', 18))
    stockTitleLabel.grid(row=1, column=1, sticky='nsew')

    # Stock input field
    try:
        # Gets values for the combobox drop down
        comboboxValues = get_combobox_values()

        stockInputField = Combobox(root, values=comboboxValues)
        stockInputField.grid(row=2, column=1)

    except OperationalError:
        stockInputField = Combobox(root)
        stockInputField.grid(row=2, column=1)

    # Target price title label
    targetPriceTitleLabel = Label(root, text='Target Price', foreground='red')
    targetPriceTitleLabel.configure(font=('Arial', 18))
    targetPriceTitleLabel.grid(row=1, column=2, sticky='nsew')

    # Target price input field
    targetPriceInputField = Entry(root)
    targetPriceInputField.grid(row=2, column=2)

    # Enter Button
    buttonEnter = Button(root, text='Enter', activeforeground='magenta', font=('Arial', 16),
                         command=lambda: collect_stock_info(root, stockInputField, targetPriceInputField, lock))
    buttonEnter.grid(row=2, column=3, sticky='nsew')

    # Clear Button
    buttonClear = Button(root, text='Clear', activeforeground='magenta', font=('Arial', 16),
                         command=lambda: clear_page(targetPriceInputField, stockInputField))
    buttonClear.grid(row=2, column=4, sticky='nsew')

    # Auto Run button
    autorunThread = threading.Thread(target=autorun, args=(stockInputField, targetPriceInputField))

    buttonAutoRun = Button(root, text='Auto Run', font=('Arial', 16), command=lambda: autorunThread.start())
    buttonAutoRun.grid(row=3, column=3, sticky='nsew')

    # Auto Run End Button
    buttonEndAutoRun = Button(root, text='End', font=('Arial', 16), command=lambda: end_auto_run())
    buttonEndAutoRun.grid(row=3, column=4, sticky='nsew')

    # Run All Button
    buttonRunAll = Button(root, text='Run All', font=('Arial', 16), command=lambda: run_all_stocks(root, lock))
    buttonRunAll.grid(row=2, column=5, sticky='nsew')


    # Run tkinter root
    root.mainloop()

    # Update widget size whenever new elements are added
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")


