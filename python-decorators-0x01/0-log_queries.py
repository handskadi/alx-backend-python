import sqlite3
import functools
from datetime import datetime

def log_queries():
    """
    This decorator will log SQL queries before executing them.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get('query', args[0] if args else None)
            if query:
                print(f"Executing SQL query: {query}")
            else:
                print("No SQL query found to log.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    """
    Fetches all users from the database based on the given query.
    :param query: SQL query to execute.
    :return: Results of the query.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
