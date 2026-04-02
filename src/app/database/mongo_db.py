from pymongo import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("Connected successfully")
except Exception as e:
    print("Connection failed:", e)
finally:
    client.close()
