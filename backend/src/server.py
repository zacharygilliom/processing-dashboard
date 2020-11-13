import pandas as pd
import sqlite3
from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

class Database:
    
    def __init__(self, path):
        self.path = path 

    def connect(self, path):
        connection = sqlite3.connect(self.path)
        cur = connection.cursor()
        return cur

    def query(self, name):
        cur = self.connect(self.path)
        rows = cur.fetchall()
        return rows

locationData = {'order_writer': ['Zachary Gilliom', 'John Smith', 'Ben James'], 'locaton': ['NU', 'JC', 'MF']}
locationDataframe = pd.DataFrame(data=locationData)

def connectDatabase():
    connection = sqlite3.connect("/home/zacharygilliom/pythonProjects/processing-dashboard/backend/data/customer_orders.db")
    cur = connection.cursor()
    return cur

def queryDatabase(cur, name):
    cur.execute("SELECT * FROM orders WHERE order_writer = ?", (name,))
    rows = cur.fetchall()
    return rows

# def getDatabase(cur):
#     cur.execute("SELECT * FROM orders")
#     rows = cur.fetchall()
#     return rows

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
    cursor = connectDatabase()
    rows = queryDatabase(cursor, name)
    # rows = getDatabase(cursor)
    col_names = ["customer_id", "company", "received", "started", "submitted", "quantity", "order_type", "order_writer"]
    data = pd.DataFrame(data=rows, columns=col_names)
    data = addCalculatedColumns(data)
    resultDataframe = data.join(locationDataframe.set_index('order_writer'), on='order_writer')
    result = resultDataframe.to_json(orient="values")
    return result 

if __name__ == '__main__':
    app.run(debug=True)

