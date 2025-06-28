import sqlite3


class DatabaseConnection(object):
    def __init__(self, db_name):
        self.db_obj = sqlite3.connect(db_name)
    def __enter__(self):
        return self.db_obj
    def __exit__(self, type, value, traceback):
        self.db_obj.close()



with DatabaseConnection('./../python-decorators-0x01/users.db') as conn:
    cursor =  conn.cursor()
    cursor.execute("SELECT * FROM users;")
    print(cursor.fetchall())
    
