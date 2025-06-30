import sqlite3

class DatabaseConnection:
    """
    A custom context manager for handling SQLite database connections.
    Automatically opens and closes the connection using `__enter__` and `__exit__`.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the database connection
        if self.connection:
            self.connection.close()
        # Handle exceptions, if any
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True  # Suppress the exception if necessary

if __name__ == "__main__":
    db_name = "users.db"
    query = "SELECT * FROM users"

    with DatabaseConnection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)
