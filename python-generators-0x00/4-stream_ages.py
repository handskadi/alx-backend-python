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

def stream_user_ages():
    """
    Generator that streams user ages from the user_data table one by one.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT age FROM user_data;")
            for row in cursor:
                yield row['age']
    except psycopg2.Error as e:
        print(f"Error streaming user ages: {e}")
    finally:
        connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate the average age.")

if __name__ == "__main__":
    calculate_average_age()
