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

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database starting from the given offset.
    :param page_size: Number of rows to fetch in each page.
    :param offset: The starting point for the query.
    :return: A list of users for the given page.
    """
    connection = connect_to_prodev()
    if not connection:
        return []

    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT user_id, name, email, age 
                FROM user_data 
                ORDER BY user_id 
                LIMIT %s OFFSET %s;
                """,
                (page_size, offset)
            )
            return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error fetching paginated users: {e}")
        return []
    finally:
        connection.close()

def lazy_pagination(page_size):
    """
    A generator to lazily fetch pages of users from the database.
    :param page_size: Number of rows in each page.
    """
    offset = 0

    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop if no more data is available
            break
        yield page
        offset += page_size


if __name__ == "__main__":
    lazy_pagination(10)