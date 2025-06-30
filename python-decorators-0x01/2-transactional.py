import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that handles opening and closing a database connection.
    It passes the connection object to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)  # Pass the connection to the decorated function
        finally:
            conn.close()
        return result
    return wrapper

def transactional(func):
    """
    This decorator will handle database transactions.
    It will Commit the transaction if the function executes successfully, else it will Rollback.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit transaction if no error occurs
            return result
        except Exception as e:
            conn.rollback()  # Rollback transaction if an error occurs
            print(f"Transaction failed, rolled back. Error: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates the email of a user in the database.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))