#!/usr/bin/python3

import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.query = query
        self.params = params
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("An error occured: ", exc_value)
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    for row in results:
        print(row)