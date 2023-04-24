from flask import Flask, render_template
from flask_restful import Api, Resource
import sqlite3
from sqlite3 import OperationalError


# Create an instance of the flasdk class
app = Flask(__name__)

# Wrap the flask object with the Api wrapper
api = Api(app)






class StockInformation(Resource):
    def get(self, searchedBy):
        # Connect to the database to retrieve the stock information
        conn = sqlite3.connect('new-data-stocks.db')
        c = conn.cursor()
        # Retrieve the stock information from the data base table
        try:
            data = c.execute('SELECT SearchedBy, Name, Price, Date, Time FROM AllStocks')
            data = data.fetchall()
        except OperationalError:
            pass

        # Empty dictionary that will be updated with the information retrieved from the AllStocks table
        dataFormatted = {}

        # Iterates through the stock information to format it into a dictionary
        for info in data:
            dict = {
                info[0]: {'name': info[1], 'price': info[2], 'date': info[3], 'time': info[4]}
            }
            dataFormatted.update(dict)
        try:
            return dataFormatted[searchedBy]
        except KeyError:
            return 'I couldnt find that!'


# Add resource to the API
api.add_resource(StockInformation, '/<string:searchedBy>')


@app.route('/')
def index():
    return render_template('/index.html')

# Connects the data template and provides information for the get request
@app.route('/data/<string:searchedBy>')
def data(searchedBy):
    dataObj = StockInformation()
    # Finds the specified key in the dictionary
    data = dataObj.get(searchedBy)
    # Renders the /data.html template which displays the specified stocks information
    return render_template('/data.html', data=data)


if __name__ == '__main__':
    app.run()

