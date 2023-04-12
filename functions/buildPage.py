from sqlite3 import OperationalError
import threading
from tkinter import Tk, Label, Frame, Entry, Button, END
from tkinter.ttk import Combobox
from functions.scrapeStock import collect_stock_info
from functions.autorunStocks import autorun
from functions.autorunStocks import end_auto_run
from functions.runAll import run_all_stocks
from functions.showPopularStocks import showPopularStocks
from functions.databaseQuerying import establish_db_connection
from functions.settings import open_settings
from functions.universalFunctions import get_combobox_values


def build_page(lock):
    def clear_page(targetPriceInputField, stockInputField, stockInformationFrame):
        # Clears the target price input field
        targetPriceInputField.delete(0, END)

        # Clears the stock input field
        stockInputField.delete(0, END)

        # Clears the stock information frame
        for widget in stockInformationFrame.winfo_children():
            widget.grid_forget()

    # Value for autorun set to false so autorun is deactivated
    autorunValue = False

    # Initialize tkinter widget
    root = Tk()

    root.title('Stock Tracker')

    ############################ Create frame for popular stocks
    framePopularStocks = Frame(root)
    showPopularStocks(root)
    framePopularStocks.grid(row=1, column=1, sticky='nsew')


    ############################# Create frame for headers
    frameHeader = Frame(root, pady=10)
    frameHeader.grid(row=2, column=1, sticky='nsew')

    # Stock title label
    stockTitleLabel = Label(frameHeader, text='Stocks', foreground='red')
    stockTitleLabel.configure(font=('Arial', 18))
    stockTitleLabel.grid(row=1, column=1, sticky='nsew')

    # Target price title label
    targetPriceTitleLabel = Label(frameHeader, text='Target Price', foreground='red')
    targetPriceTitleLabel.configure(font=('Arial', 18))
    targetPriceTitleLabel.grid(row=2, column=1, sticky='nsew')


    ############################ Create frame for input fields
    userInputFrame = Frame(root, pady=10)
    userInputFrame.grid(row=2, column=2, sticky='nsew')

    # Stock input field
    try:
        # Gets values for the combobox drop down
        comboboxValues = get_combobox_values()

        stockInputField = Combobox(userInputFrame, values=comboboxValues)
        stockInputField.grid(row=1, column=1, sticky='nsew')
        stockInputField.bind('<Return>', lambda event: collect_stock_info(stockInformationFrame, stockInputField, targetPriceInputField, lock))

    except OperationalError:
        stockInputField = Combobox(userInputFrame)
        stockInputField.grid(row=1, column=1, sticky='nsew')
        stockInputField.bind('<Return>', lambda event: collect_stock_info(stockInformationFrame, stockInputField,targetPriceInputField, lock))

    # Target price input field
    targetPriceInputField = Entry(userInputFrame)
    targetPriceInputField.grid(row=2, column=1, sticky='nsew')
    targetPriceInputField.bind('<Return>', lambda event: collect_stock_info(stockInformationFrame, stockInputField, targetPriceInputField, lock))



    ########################### Create frame for buttons
    frameButtons = Frame(root, pady=10)
    frameButtons.grid(row=2, column=3, sticky='nsew')

    # Enter Button
    buttonEnter = Button(frameButtons, text='Enter', activeforeground='magenta', font=('Arial', 16),
                         command=lambda: collect_stock_info(stockInformationFrame, stockInputField, targetPriceInputField, lock))
    buttonEnter.grid(row=1, column=1, sticky='nsew')

    # Clear Button
    buttonClear = Button(frameButtons, text='Clear', activeforeground='magenta', font=('Arial', 16), command=lambda: clear_page(targetPriceInputField, stockInputField, stockInformationFrame))
    buttonClear.grid(row=1, column=2, sticky='nsew')

    # Run All Button
    buttonRunAll = Button(frameButtons, text='Run All', activeforeground='magenta', font=('Arial', 16), command=lambda: run_all_stocks(stockInformationFrame, lock))
    buttonRunAll.grid(row=1, column=3, sticky='nsew')

    # Auto Run button
    autorunThread = threading.Thread(target=autorun, args=(stockInputField, targetPriceInputField))

    buttonAutoRun = Button(frameButtons, text='Auto Run', activeforeground='magenta', font=('Arial', 16), command=lambda: autorunThread.start())
    buttonAutoRun.grid(row=2, column=1, sticky='nsew')

    # Auto Run End Button
    buttonEndAutoRun = Button(frameButtons, text='End', activeforeground='magenta', font=('Arial', 16), command=lambda: end_auto_run())
    buttonEndAutoRun.grid(row=2, column=2, sticky='nsew')

    # Settings Button
    buttonSettings = Button(frameButtons, text='Settings', activeforeground='magenta', font=('Arial', 16), command=lambda: open_settings(root))
    buttonSettings.grid(row=2, column=3, sticky='nsew')

    ########### Create frame for stock information
    stockInformationFrame = Frame(root, bg='black')
    stockInformationFrame.grid(row=3, column=1, columnspan=3, sticky='nsew')




    # Run tkinter root
    root.mainloop()

    # Update widget size whenever new elements are added
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")


