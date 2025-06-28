import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def connect_db(*args, **kwargs):
      conn = sqlite3.connect('users.db')
      try:
        result =  func(conn, *args, **kwargs)
      finally:
         conn.close()
      return result
    return connect_db

def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        cache_key = tuple(kwargs.items())
        if cache_key not in wrapper_cache.cache:
            wrapper_cache.cache[cache_key] = func(*args, **kwargs)
        return wrapper_cache.cache[cache_key]
    wrapper_cache.cache = query_cache
    return wrapper_cache             


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")