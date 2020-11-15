import pandas as pd
import sqlite3
from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

DATABASE_PATH = "/home/zacharygilliom/pythonProjects/processing-dashboard/backend/data/customer_orders.db"

class Database:
    
    def __init__(self, path):
        self.path = path 

    def connect(self):
        connection = sqlite3.connect(self.path)
        return connection

    def query(self, name):
        connection = self.connect(self.path)
        cur = connection.cursor() 
        cur.execute("SELECT * FROM orders WHERE order_writer = ?", (name,))
        rows = cur.fetchall()
        cur.close()
        return rows

locationData = {'order_writer': ['Zachary Gilliom', 'John Smith', 'Ben James'], 'locaton': ['NU', 'JC', 'MF']}
locationDataframe = pd.DataFrame(data=locationData)

def addCalculatedColumns(dataframe):
    # Add our 3 columns and convert the timedelta series to include on the days value.
    dataframe['received'] = pd.to_datetime(dataframe['received'], format='%Y-%m-%d %H:%M:%S')
    dataframe['started'] = pd.to_datetime(dataframe['started'], format='%Y-%m-%d %H:%M:%S')
    dataframe['submitted'] = pd.to_datetime(dataframe['submitted'], format='%Y-%m-%d %H:%M:%S')

    dataframe['receivedtostart'] = dataframe.started - dataframe.received
    dataframe['receivedtostart'] = dataframe['receivedtostart'].dt.days

    dataframe['receivedtosubmit']= dataframe.submitted - dataframe.received
    dataframe['receivedtosubmit'] = dataframe['receivedtosubmit'].dt.days

    dataframe['starttosubmit']= dataframe.submitted - dataframe.received
    dataframe['starttosubmit'] = dataframe['starttosubmit'].dt.days

    return dataframe

@app.route('/<string:name>', methods=['GET'])
def namefunction(name):
    database = Database(DATABASE_PATH)
    rows = database.query(name)
    col_names = ["customer_id", "company", "received", "started", "submitted", "quantity", "order_type", "order_writer"]
    data = pd.DataFrame(data=rows, columns=col_names)
    data = addCalculatedColumns(data)
    resultDataframe = data.join(locationDataframe.set_index('order_writer'), on='order_writer')
    result = resultDataframe.to_json(orient="values")
    return result 

if __name__ == '__main__':
    app.run(debug=True)

