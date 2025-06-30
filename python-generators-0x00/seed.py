import psycopg2
import csv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connect_db():
    """
    Connects to the PostgreSQL server (default database).
    """
    try:
        connection = psycopg2.connect(
            dbname="ALX_prodev",
            user="alx",
            password="alx",
            host="localhost",
            port="5432"
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # print("connection successful")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def create_database(connection):
    """
    Creates the database 'ALX_prodev' if it does not exist.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ALX_prodev';")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE ALX_prodev;"))
                print("Database 'ALX_prodev' created.")
            else:
                print("Database ALX_prodev is present.")
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")

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
        # print("Connected to the 'ALX_prodev' database.")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """
    Creates the table 'user_data' if it does not exist.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    age DECIMAL NOT NULL
                );
            """)
            connection.commit()
            print("Table user_data created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    """
    Inserts data into the 'user_data' table if it does not already exist.
    :param connection: The PostgreSQL connection object.
    :param data: a csv file containing the data to be inserted
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            with connection.cursor() as cursor:
                for row in reader:
                    cursor.execute("""
                        INSERT INTO user_data (name, email, age)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (email) DO NOTHING;
                    """, (row['name'], row['email'], row['age']))
            connection.commit()
            # print("Data from csv file inserted.")
    except psycopg2.Error as e:
        print(f"Error inserting data from csv file: {e}")

if __name__ == "__main__":
    # Step 1: Connect to the default PostgreSQL database
    conn = connect_db()
    if conn:
        # Step 2: Create the 'ALX_prodev' database if it doesn't exist
        create_database(conn)
        conn.close()

    # Step 3: Connect to the 'ALX_prodev' database
    conn_prodev = connect_to_prodev()
    if conn_prodev:
        # Step 4: Create the 'user_data' table
        create_table(conn_prodev)

        # Step 5: Insert sample data from csv file
        csv_file_path = 'user_data.csv'
        insert_data(conn_prodev, csv_file_path)

        conn_prodev.close()
