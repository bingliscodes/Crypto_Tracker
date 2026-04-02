from pymongo import MongoClient
from src.app.utils.singleton import SingletonMeta


class MongoDBConnection(metaclass=SingletonMeta):
    def __init__(self, uri: str):
        self._connection = MongoClient(uri)

    def get_connection(self):
        if self._connection is None:
            raise ConnectionError("MongoDB Connection has been closed.")
        return self._connection

    def close_connection(self):
        self._connection.close()
        self._connection = None
