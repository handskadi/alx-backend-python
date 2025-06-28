import sqlite3


class ExecuteQuery  (object):
    def __init__(self, db_name, query, filter):
        self.db_conn = sqlite3.connect(db_name)
        self.query = query
        self.filter = filter
    def __enter__(self):
        cursor = self.db_conn.cursor()
        cursor.execute(self.query, (self.filter,))
        return cursor.fetchall()
    def __exit__(self, type, value, traceback):
        self.db_conn.close()


with ExecuteQuery('./../python-decorators-0x01/users.db', "SELECT * FROM users WHERE age > ?", 25) as db_result:
    print(db_result)