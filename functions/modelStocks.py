from tkinter import Tk
from functions.databaseQuerying import establish_db_connection
from functions.universalFunctions import get_all_prices, plotGraph


# Shows the graph containing price data
def showPlot(stock):

    # create a new tkinter root that will display the graph
    newroot = Tk()

    # Connect to the database
    c = establish_db_connection()

    # Get the data for the graph
    graphData = get_all_prices(c[0], stock)
    print(stock)

    # Plot the values and create the graph
    plotGraph(newroot, stock, graphData[0], graphData[1], graphData[2])


