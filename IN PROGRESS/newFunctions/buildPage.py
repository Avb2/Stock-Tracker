from tkinter import *
from tkinter.ttk import Combobox
from newFunctions.scrapeStock import collect_stock_info


def build_page(lock):
    def clear_page(root, lock):
        def rebuild_page():
            build_page(lock)

        root.destroy()
        rebuild_page()

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
                         command=lambda: clear_page(root, lock))
    buttonClear.grid(row=2, column=4, sticky='nsew')

    # Run tkinter root
    root.mainloop()

    # Update widget size whenever new elements are added
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")
