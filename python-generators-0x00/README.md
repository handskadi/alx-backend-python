## Seed.py Functionality

The `seed.py` script contains functions to set up the database and populate it with data from `user_data.csv`. Here's a breakdown of the functions:

*   **connect\_db()**: Establishes a connection to the MySQL database 'ALX_prodev'.
*   **create_database(connection)**: Creates the 'ALX_prodev' database if it doesn't already exist.
*   **connect_to_prodev()**: Connects to the ALX_prodev database.
*   **create_table(connection)**: Creates the 'user_data' table in the database, based on the schema defined in `models.py`.
*   **insert_data(connection, data)**: Reads data from the `user_data.csv` file and inserts it into the 'user_data' table. It skips duplicate entries based on email and handles potential `ValueError` exceptions during data insertion.