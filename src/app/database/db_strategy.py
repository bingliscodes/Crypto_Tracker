from dotenv import load_dotenv
from abc import ABC, abstractmethod
import pymongo
from sqlalchemy import select, desc

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
        db = MongoDBConnection().get_connection()[
            "crypto_db"
        ]  # Creates a DB called crypto_db if it doesn't already exist
        db["crypto_prices"].insert_many(
            data
        )  # Selects the collection called "crypto_prices"

    def get_latest(self, symbol: str) -> dict | None:
        db = MongoDBConnection().get_connection()["crypto_db"]
        res = db["crypto_prices"].find_one(
            {"symbol": symbol}, sort={"timestamp": pymongo.DESCENDING}
        )
        return res


class PostgresStorage(StorageStrategy):
    def save(self, data: list[dict]):
        with SessionLocal() as session:
            records = [CryptoPrice(**coin) for coin in data]
            session.add_all(records)
            session.commit()

    def get_latest(self, symbol: str) -> dict | None:
        with SessionLocal() as session:
            stmt = (
                select(CryptoPrice)
                .where(CryptoPrice.symbol == symbol)
                .order_by(desc(CryptoPrice.timestamp))
                .limit(1)
            )
            return session.execute(stmt).scalars().first()


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
