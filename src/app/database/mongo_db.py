from pymongo import MongoClient
from src.app.utils.singleton import SingletonMeta


class MongoDBConnection(metaclass=SingletonMeta):
    def __init__(self, uri: str):
        self._connection = MongoClient(uri)

    def get_connection(self):
        return self._connection

    def close_connection(self):
        self._connection.close()
        self._connection = None


uri = "mongodb://localhost:27017"
client = MongoDBConnection(uri)

try:
    client._connection.admin.command("ping")
    print("Connected successfully")
except Exception as e:
    print("Connection failed:", e)
finally:
    client._connection.close()
