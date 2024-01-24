import psycopg2
import time
from db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def get_db_connection():
    try:
        # Establish a connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn

    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
        return None

def retry_db_connection(func, max_retries=3, retry_delay=5, *args, **kwargs):
    retries = 0

    while retries < max_retries:
        try:
            connection = func(*args, **kwargs)
            if connection is not None:
                return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")

        print(f"Retrying in {retry_delay} seconds... (Attempt {retries + 1}/{max_retries})")
        time.sleep(retry_delay)
        retries += 1

    print(f"Maximum retries reached. Unable to establish a database connection.")
    return None
