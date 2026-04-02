from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from sqlalchemy import insert

from src.app.database.postgres_db import SessionLocal
from src.app.models.crypto_price import CryptoPrice
from .mongo_db import MongoDBConnection

load_dotenv()

# This is where I will create the interface to select between the two


# --- Strategy Interface ---
class StorageStrategy(ABC):
    @abstractmethod
    def save(self, data: list[dict]):
        pass

    @abstractmethod
    def get_latest(self, symbol: str) -> dict | None:
        pass


# --- Concrete Strategies ---
class MongoDBStorage(StorageStrategy):
    def save(self, data: list[dict]):
        pass

    def get_latest(self, symbol: str) -> dict | None:
        pass


class PostgresStorage(StorageStrategy):
    def save(self, data: list[dict]):
        with SessionLocal() as session:
            records = [CryptoPrice(**coin) for coin in data]
            session.add_all(records)
            session.commit()

    def get_latest(self, symbol: str) -> dict | None:
        try:
            query = f"""SELECT * FROM crypto_prices WHERE symbol = '{symbol}' ORDER BY timestamp ASC """
            with self._conn.cursor as cursor:
                row = cursor.execute(query).fetchone()
                return row
        finally:
            self._postgres._pool.putconn(self._conn)


# --- Context ---
class DataStorage:
    def __init__(self):
        self._storage_strategy: StorageStrategy | None = None

    def set_storage_strategy(self, strategy: StorageStrategy):
        self._storage_strategy = strategy

    def save(self, data: list[dict]):
        if self._storage_strategy is None:
            return "No storage strategy set!"

        return self._storage_strategy.save(data)

    def get_latest(self, symbol: str) -> dict | None:
        if self._storage_strategy is None:
            return "No storage strategy set!"

        return self._storage_strategy.get_latest(symbol)
