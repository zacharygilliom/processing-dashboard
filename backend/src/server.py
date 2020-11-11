import pandas as pd
import sqlite3
from flask import Flask
from flask import jsonify

app = Flask(__name__)


def connectDatabase():
    connection = sqlite3.connect("/home/zacharygilliom/pythonProjects/processing-dashboard/backend/data/customer_orders.db")
    cur = connection.cursor()
    return cur

def addCalculatedColumns(dataframe):
    # Add our 3 columns and convert the timedelta series to include on the days value.
    dataframe['received'] = pd.to_datetime(dataframe['received'], format='%Y-%m-%d %H:%M:%S')
    dataframe['started'] = pd.to_datetime(dataframe['started'], format='%Y-%m-%d %H:%M:%S')
    dataframe['submitted'] = pd.to_datetime(dataframe['submitted'], format='%Y-%m-%d %H:%M:%S')

    dataframe['receivedtostart'] = dataframe.started - dataframe.received
    dataframe['receivedtostart'] = dataframe['receivedtostart'].dt.days

    dataframe['receivedtosubmit'] = dataframe.submitted - dataframe.received
    dataframe['receivedtosubmit'] = dataframe['receivedtosubmit'].dt.days

    dataframe['starttosubmit'] = dataframe.submitted - dataframe.received
    dataframe['starttosubmit'] = dataframe['starttosubmit'].dt.days

    return dataframe

@app.route('/<string:name>', methods=['GET'])
def namefunction(name):
    cur = connectDatabase()
    cur.execute("SELECT * FROM orders WHERE order_writer = ?", (name,))
    rows = cur.fetchall()
    col_names = ["customer_id", "company", "received", "started", "submitted", "quantity", "order_type", "order_writer"]
    data = pd.DataFrame(data=rows, columns=col_names)
    data = addCalculatedColumns(data)
    print(data)
    result = data.to_json(orient="values")
    return result 

if __name__ == '__main__':
    app.run(debug=True)

