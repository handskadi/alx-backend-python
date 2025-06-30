import psycopg2
def connect_to_prodev():
    """
    Connects to the 'ALX_prodev' database.
    """
    try:
        connection = psycopg2.connect(
            dbname="ALX_prodev",
            user="alx",
            password="alx",
            host="localhost",
            port="5432"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def stream_users():
    """
    Streams rows from the 'user_data' table one by one using a generator.
    """
    connection = connect_to_prodev()  # Establish connection to the database

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        
        # Fetch and yield rows one by one using a while loop
        while True:
            row = cursor.fetchone()  # Fetch the next row
            if row is None:
                break  # Exit the loop when no rows are left
            yield row  # Yield the current row
    except Exception as e:
        print(f"Error streaming users: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Iterate over the generator function and print only the first 6 rows
    from itertools import islice
    for user in islice(stream_users(), 6):
        print(user)