from dotenv import load_dotenv
import os
import psycopg2

from src.app.utils.singleton import SingletonMeta

load_dotenv()

db_url = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("DB_NAME")}"


class PostgresConnection(metaclass=SingletonMeta):
    def __init__(self, uri: str):
        self._pool = psycopg2.pool.simpleConnectionPool(minconn=1, maxconn=10, dsn=uri)

        self._initialize_schema()

    def _initialize_schema(self):
        conn = self._pool.getconn()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS crypto_prices (
                               id VARCHAR,
                               symbol VARCHAR,
                               price FLOAT,
                               currency VARCHAR,
                               timestamp TIMESTAMP
                    )
                               """
                )
            conn.commit()
        finally:
            self._pool.putconn(conn)

    def get_connection(self):
        return self._pool.get_conn()

    def release_connection(self, conn):
        self._pool.putconn(conn)

    def close_all(self):
        self._pool.closeall()
