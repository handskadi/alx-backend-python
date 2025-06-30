import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection and create a cursor
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        # Execute the query
        self.cursor.execute(self.query, self.params or [])
        return self.cursor  # Return the cursor for fetching results

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # Handle exceptions, if any
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True  # Suppress the exception if necessary

# Using the custom context manager
if __name__ == "__main__":
    db_name = "users.db"  # Database file
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)  # Parameter for the query

    with ExecuteQuery(db_name, query, params) as cursor:
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)
