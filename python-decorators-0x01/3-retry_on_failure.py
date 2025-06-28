import time
import sqlite3 
import functools

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

def retry_on_failure(retries, delay):
    def decorator_retry(func):
      @functools.wraps(func)
      def retry(*args, **kwargs):
        for attempt in range(retries):
            try:
              return func(*args, **kwargs)
            except sqlite3.Error as e:
              time.sleep(delay)
      return retry
    return decorator_retry

     

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)