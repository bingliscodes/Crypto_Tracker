from fastapi import FastAPI
from dotenv import load_dotenv
import os

from src.app.database.mongo_db import MongoDBConnection
from src.app.database.postgres_db import engine, Base
import src.app.models.crypto_price

load_dotenv()

Base.metadata.create_all(engine)
mongo = MongoDBConnection(os.getenv("MONGO_URI"))


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
