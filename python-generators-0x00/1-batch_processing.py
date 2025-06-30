import psycopg2
from psycopg2.extras import DictCursor

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

def stream_users_in_batches(batch_size):
    """
    Generator to fetch users in batches from the user_data table.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT COUNT(*) FROM user_data;")
            total_rows = cursor.fetchone()[0]

            for offset in range(0, total_rows, batch_size):
                cursor.execute(
                    """
                    SELECT user_id, name, email, age 
                    FROM user_data 
                    ORDER BY user_id 
                    LIMIT %s OFFSET %s;
                    """,
                    (batch_size, offset)
                )
                rows = cursor.fetchall()
                yield rows
    except psycopg2.Error as e:
        print(f"Error fetching batches: {e}")
    finally:
        connection.close()

def batch_processing(batch_size):
    """
    Processes users in batches to filter users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(f"User: {user['name']}, Email: {user['email']}, Age: {user['age']}")

if __name__ == "__main__":
    batch_processing(batch_size=3)
