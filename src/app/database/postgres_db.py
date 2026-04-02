from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

db_url = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("DB_NAME")}"
try:
    connection = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port="5432",
        database=os.getenv("DB_NAME"),
    )

    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS CRYPTO_PRICES (id VARCHAR, symbol VARCHAR, price FLOAT, currency VARCHAR, timestamp TIMESTAMP)"
    )

    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if connection:
        cursor.close()
        connection.close()
