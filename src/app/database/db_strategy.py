from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod
from pydantic import BaseModel
from psycopg2.extras import execute_values
from datetime import datetime, timezone

from .postgres_db import PostgresConnection
from .mongo_db import MongoDBConnection

load_dotenv()

# This is where I will create the interface to select between the two


class CoinData(BaseModel):
    name: str
    symbol: str
    price: str


class PriceData(BaseModel):
    data: list[CoinData]


# --- Strategy Interface ---
class StorageStrategy(ABC):
    @abstractmethod
    def save(self, data: PriceData):
        pass

    @abstractmethod
    def get_latest(self, symbol: str) -> CoinData | None:
        pass


# --- Concrete Strategies ---
class MongoDBStorage(StorageStrategy):
    def save(self, data: PriceData):
        pass

    def get_latest(self, symbol: str) -> CoinData | None:
        pass


class PostgresStorage(StorageStrategy):
    def save(self, data: PriceData):
        postgres = PostgresConnection(os.getenv("POSTGRES_URI"))
        conn = postgres.get_connection()
        try:
            values = [
                (
                    coin["name"],
                    coin["symbol"],
                    coin["price"],
                    datetime.now(timezone.utc),
                )
                for coin in data
            ]
            query = (
                "INSERT INTO crypto_prices (name, symbol, price, timestamp) VALUES %s"
            )
            with conn.cursor() as cursor:
                execute_values(cursor, query, values)
            conn.commit()
        finally:
            postgres._pool.putconn(conn)

    def get_latest(self, symbol: str) -> CoinData | None:
        pass


# --- Context ---
class DataStorage:
    def __init__(self):
        self._storage_strategy: StorageStrategy | None = None

    def set_storage_strategy(self, strategy: StorageStrategy):
        self._storage_strategy = strategy

    def save(self, data: PriceData):
        if self._storage_strategy is None:
            return "No storage strategy set!"

        return self._storage_strategy.save(data)

    def get_latest(self, symbol: str) -> CoinData | None:
        if self._storage_strategy is None:
            return "No storage strategy set!"

        return self._storage_strategy.get_latest(symbol)
