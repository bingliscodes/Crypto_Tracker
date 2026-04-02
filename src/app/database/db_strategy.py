from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod
from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy import insert

from src.app.database.postgres_db import SessionLocal
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
        with SessionLocal() as session:
            session.execute(insert(CoinData), data)
            session.commit()

    def get_latest(self, symbol: str) -> CoinData | None:
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

    def save(self, data: PriceData):
        if self._storage_strategy is None:
            return "No storage strategy set!"

        return self._storage_strategy.save(data)

    def get_latest(self, symbol: str) -> CoinData | None:
        if self._storage_strategy is None:
            return "No storage strategy set!"

        return self._storage_strategy.get_latest(symbol)
