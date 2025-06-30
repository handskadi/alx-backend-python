import sqlite3
import functools

# this is a global dictionary to store cached query results
query_cache = {}

def cache_query(func):
    """
    A decorator that caches the results of a database query.
    The Caches are keyed by the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or args[1]  # Get the query string
        if query in query_cache:
            print("Fetching result from cache...")
            return query_cache[query]  # Return the cached result
        print("Querying database and caching result...")
        result = func(*args, **kwargs)  # Execute the function
        query_cache[query] = result  # Caching the result
        return result
    return wrapper

def with_db_connection(func):
    """
    A decorator that handles opening and closing a database connection.
    It will pass the connection object to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database based on the given query.
    Uses caching to avoid redundant calls for the same query.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()