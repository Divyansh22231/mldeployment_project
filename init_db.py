import mysql.connector

try:
    # Connect to MySQL server without selecting a database
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="9555805060"
    )
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS ml_project")
    print("Database 'ml_project' checked/created.")

    # Use the database
    cursor.execute("USE ml_project")

    # Create the predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        study_hours FLOAT NOT NULL,
        prediction FLOAT NOT NULL,
        result VARCHAR(10) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Table 'predictions' checked/created.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
