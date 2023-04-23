from flask import Flask
from flask_restful import Api, Resource
import sqlite3

app = Flask(__name__)

api = Api(app)

conn = sqlite3.connect('new-data-stocks.db')
c = conn.cursor()

data = c.execute('SELECT SearchedBy, Name, Price, Date, Time FROM AllStocks')
data = data.fetchall()


dataFormatted = {}

for info in data:
    dict = {
        info[0]: {'name': info[1], 'price': info[2], 'date': info[3], 'time': info[4]}
    }
    dataFormatted.update(dict)

print(dataFormatted)


class StockInformation(Resource):
    def get(self, searchedBy):
        try:
            return dataFormatted[searchedBy]
        except KeyError:
            return 'I couldnt find that!'


api.add_resource(StockInformation, '/<string:searchedBy>')

if __name__ == '__main__':
    app.run()

