from tkinter import *
from tkinter.ttk import Combobox
from newFunctions.scrapeStock import collect_stock_info

# Initialize tkinter widget
root = Tk()
root.columnconfigure(1, pad=20)

# Stock title label
stockTitleLabel = Label(root, text='Stocks', foreground='red')
stockTitleLabel.configure(font=('Arial', 16))
stockTitleLabel.grid(row=1, column=1)

# Stock input field
stockInputField = Combobox(root)
stockInputField.grid(row=2, column=1)

# Target price title label
targetPriceTitleLabel = Label(root, text='Target Price', foreground='red')
targetPriceTitleLabel.configure(font=('Arial', 16))
targetPriceTitleLabel.grid(row=1, column=2)

# Target price input field
targetPriceInputField = Entry(root)
targetPriceInputField.grid(row=2, column=2)

# Enter Button
buttonEnter = Button(root, text='Enter', activeforeground='magenta', command=lambda: collect_stock_info(root, stockInputField, targetPriceInputField))
buttonEnter.grid(row=2, column=3)

# Run tkinter root
root.mainloop()
