from fastapi import FastAPI
from dotenv import load_dotenv
import os

from src.app.database.mongo_db import MongoDBConnection
from src.app.database.postgres_db import engine, Base
from src.app.database.db_strategy import (
    StorageStrategy,
    PostgresStorage,
    MongoDBStorage,
)
from src.app.data_retrieval.data_strategy import (
    FetchStrategy,
    CoinGeckoStrategy,
    CoinMarketCapStrategy,
    MockStrategy,
)

load_dotenv()

Base.metadata.create_all(engine)
mongo = MongoDBConnection(os.getenv("MONGO_URI"))


class PriceService:
    def __init__(self):
        self._storage_strategy: StorageStrategy | None = None
        self._fetch_strategy: FetchStrategy | None = None

    def set_storage_strategy(self, strategy: StorageStrategy):
        self._storage_strategy = strategy

    def set_fetch_strategy(self, strategy: FetchStrategy):
        self._fetch_strategy = strategy

    def get_prices_and_save(self):
        if self._fetch_strategy is None or self._storage_strategy is None:
            return "Make sure to set both fetch and storage strategies first!"

        data = self._fetch_strategy.fetch_all_prices()
        self._storage_strategy.save(data)

    def get_latest(self, symbol: str) -> dict:
        return self._storage_strategy.get_latest(symbol)


app_interface = PriceService()
app_interface.set_fetch_strategy(CoinMarketCapStrategy())
app_interface.set_storage_strategy(PostgresStorage())
print("Getting latest btc...", app_interface.get_latest("btc"))

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
