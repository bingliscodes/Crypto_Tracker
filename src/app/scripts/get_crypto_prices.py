import os
from dotenv import load_dotenv

from src.app.database.db_strategy import MongoDBStorage, PostgresStorage
from src.app.data_retrieval.data_strategy import (
    CoinMarketCapStrategy,
    CoinGeckoStrategy,
)
from src.app.main import PriceService

load_dotenv()

if os.getenv("STORAGE_MODE").lower() == "mongodb":
    storage_mode = MongoDBStorage()

elif os.getenv("STORAGE_MODE").lower() == "postgres":
    storage_mode = PostgresStorage()

if os.getenv("DATA_SOURCE").lower() == "coinmarketcap":
    fetch_strategy = CoinMarketCapStrategy()

elif os.getenv("DATA_SOURCE").lower() == "coingecko":
    fetch_strategy = CoinGeckoStrategy()

service = PriceService()
service.set_storage_strategy(storage_mode)
service.set_fetch_strategy(fetch_strategy)
service.get_prices_and_save()
