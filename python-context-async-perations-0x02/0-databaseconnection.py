#!/usr/bin/python3

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("An error occured: ", exc_value)
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def setup_database():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email VARCHAR(50), age INTEGER)")
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (1, 'Alice', 'alile@yahoo.com', 30), (2, 'Bob', 'bob@gmail.com', 24)")
        conn.commit()

setup_database()

with DatabaseConnection("users.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)