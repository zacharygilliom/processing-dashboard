import pandas as pd
import sqlite3
from flask import Flask
from flask import jsonify

app = Flask(__name__)


def connectDatabase():
    connection = sqlite3.connect("/home/zacharygilliom/pythonProjects/processing-dashboard/backend/data/customer_orders.db")
    cur = connection.cursor()
    return cur
 

@app.route('/<string:name>', methods=['GET'])
def (name):
    cur = connectDatabase()
    cur.execute("SELECT * FROM orders WHERE order_writer = ?", (name,))
    rows = cur.fetchall()
    col_names = ["customer_id", "company", "received", "started", "submitted", "quantity", "order_type", "order_writer"]
    data = pd.DataFrame(data=rows, columns=col_names)
    print(data)
    connection.close()
    return jsonify("Hello " + name)

if __name__ == '__main__':
    app.run(debug=True)

