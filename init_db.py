import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Connect to PostgreSQL server (default database 'postgres' or specific)
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD'),
        dbname=os.environ.get('DB_NAME', 'postgres')
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Get the target database name
    target_db = os.environ.get('DB_NAME', 'ml_project')

    # Create database if it doesn't exist
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (target_db,))
    exists = cursor.fetchone()
    if not exists:
        try:
            cursor.execute(f"CREATE DATABASE {target_db}")
            print(f"Database '{target_db}' checked/created.")
        except psycopg2.Error as e:
            print(f"Could not create database (this is normal on Render): {e}")
    else:
        print(f"Database '{target_db}' already exists.")
        
    cursor.close()
    conn.close()

    # Connect to the new database
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD'),
        dbname=os.environ.get('DB_NAME', 'ml_project')
    )
    cursor = conn.cursor()

    # Create the predictions table
    # Note: AUTO_INCREMENT in MySQL is SERIAL in PostgreSQL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        study_hours FLOAT NOT NULL,
        prediction FLOAT NOT NULL,
        result VARCHAR(10) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("Table 'predictions' checked/created.")

except psycopg2.Error as err:
    print(f"Error: {err}")
finally:
    if 'cursor' in locals() and not cursor.closed:
        cursor.close()
    if 'conn' in locals() and not conn.closed:
        conn.close()
