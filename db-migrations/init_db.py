import os
import subprocess
import psycopg2
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

# Read Postgres configuration from environment variables
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PASSWORD_ENCODED = quote(POSTGRES_PASSWORD)

# Check if a database already exists
def database_exists(database_name):
    encoded_db_name = quote(database_name)
    check_command = [
        "psql",
        "-U", POSTGRES_USER,
        "-p", POSTGRES_PASSWORD_ENCODED,
        "-h", POSTGRES_HOST,
        "-c", f"SELECT 1 FROM pg_database WHERE datname='{encoded_db_name}'"
    ]
    result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "1 row" in result.stdout

# Create database for each organization using dbmate
def create_database_with_dbmate(database_name):
    # Check if the database already exists
    if database_exists(database_name):
        print(f"Database {database_name} already exists. Skipping creation.")
        return
    
    conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )

    # Ensure the uuid-ossp extension is available
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        conn.commit()
    conn.close()

    # URL-encode the database name
    encoded_org_name = quote(database_name)
    dbmate_command = [
        "dbmate",
        "-u", f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD_ENCODED}@{POSTGRES_HOST}:{POSTGRES_PORT}/{encoded_org_name}?sslmode=disable",
        "-d", "migrations/database-data-schemas",
        "up"
    ]
    try:
        subprocess.run(dbmate_command, check=True)
        print(f"Database created for: {database_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create database {database_name}: {e}")
        raise


def main():
    try:
        create_database_with_dbmate("attentions_ai")
        print("Database and migrations setup successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()