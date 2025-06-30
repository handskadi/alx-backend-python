import sqlite3
import functools
from datetime import datetime

def with_db_connection(func):
    """
    This decorator handles opening and closing of a database connection.
    It will then pass the connection object to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # open a connection
        try:
            result = func(conn, *args, **kwargs)  # pass the connection to the decorated function
        finally:
            conn.close()  # close the connection
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user by their ID from the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()