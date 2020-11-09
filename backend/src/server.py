import pandas as pd
import sqlite3

def connectDatabase():
    connection = sqlite3.connect("/home/zacharygilliom/goProjects/processing-dashboard/backend/data/customer_orders.db")
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM orders").fetchall()
    print(rows)


connectDatabase()

