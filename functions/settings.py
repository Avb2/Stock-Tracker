from sqlite3 import OperationalError
from tkinter import Frame, Label, Button, Entry
from functions.universalFunctions import establish_db_connection, create_title_for_db, collect_and_split_stock

def close_settings(settingsFrame):
        settingsFrame.grid_forget()


def open_settings(root):
    # Collects the user inputs from the entry widgets
    def collect_group_stock_inputs():
        stockGroupName = stockGroupInput.get()
        stocksInGroupNames = (stockEntryInput.get()).split(',')

        return stockGroupName, stocksInGroupNames

    def add_stocks_to_groups():
        def create_group_table():
            # Connect to the new-data-stocks.db file
            c = establish_db_connection()

            # Attempts to create the stock group table, which stores the group name and stock names that are within the group
            try:
                c[0].execute(f'''CREATE TABLE {title}
                                           (
                                           StockGroup,
                                           Name
                                           )''')
                c[1].commit()

                print(f'{title} group table created')
            # If the table already exists, the below message will be printed in the terminal
            except OperationalError:
                print(f'Operational Error: Could not create {title} table, it already exists.')

            try:
                c[0].execute(f'''CREATE TABLE AllGroups
                                           (
                                           GroupName,
                                           Stocks
                                           )''')
                c[1].commit()

                print(f'AllGroups table created')

            # If the table already exists, the below message will be printed in the terminal
            except OperationalError:
                print(f'Operational Error: Could not create AllGroups table, it already exists.')

            c[1].close()

        def add_values_to_group_table(stockName):
            c = establish_db_connection()
            # Adds the values to the group database table
            c[0].execute(f'''INSERT INTO {title} VALUES
                                            (
                                            "{title}",
                                            "{stockName}"
                                            )''')
            c[1].commit()
########################

            c[0].execute(f'''INSERT INTO AllGroups VALUES
                                                        (
                                                        "{title}",
                                                        "{stockName}"
                                                        )''')
            c[1].commit()

            print(f'Values have been added to AllGroups table.')

        # Collects the inputs from the settings entry widgets
        collectGroupStockInputs = collect_group_stock_inputs()

        # Separates the values into their own variables
        stockGroupName = collectGroupStockInputs[0]
        stocksInGroupNames = collectGroupStockInputs[1]

        # Creates a title from the stockGroupName entry widget by removing the bad characters
        title = create_title_for_db(str(stockGroupName))

        # Create the table for the group
        create_group_table()

        for name in stocksInGroupNames:
            add_values_to_group_table(name)




    ############### Create frame for settings
    settingsFrame = Frame(root, borderwidth=2, relief='solid', pady=3)
    settingsFrame.grid(row=2, rowspan=3, column=4, sticky='nsew')

    # Button to close the settings frame
    buttonCloseSavings = Button(settingsFrame, text='X', command=lambda: close_settings(settingsFrame))
    buttonCloseSavings.grid(row=1, column=1)

    # Settings title label
    settingsTitleLabel = Label(settingsFrame, text='Settings', justify='center', font=('Arial', 16))
    settingsTitleLabel.grid(row=1, column=2, columnspan=2, sticky='nsew')

    # Title label for the input field where the user inputs the name of the groiup they are creating
    stockGroupTitle = Label(settingsFrame, text='Group Name')
    stockGroupTitle.grid(row=2, column=1, sticky='nsew')

    # Input field where the user inputs the name of the group they are creating
    stockGroupInput = Entry(settingsFrame)
    stockGroupInput.grid(row=2, column=2, columnspan=2, sticky='nsew')

    ## Stock input field
    stockEntryTitle = Label(settingsFrame, text='Stock Names')
    stockEntryTitle.grid(row=3, column=1, sticky='nsew')

    stockEntryInput = Entry(settingsFrame)
    stockEntryInput.grid(row=3, column=2, columnspan=2, sticky='nsew')

    # Stock group enter button
    buttonEnterStockGroups = Button(settingsFrame, text='Enter', command=lambda: add_stocks_to_groups())
    buttonEnterStockGroups.grid(row=4, column=1, columnspan=3, sticky='nsew')


