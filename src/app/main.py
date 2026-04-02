from fastapi import FastAPI
from dotenv import load_dotenv
import os

from src.app.database.mongo_db import MongoDBConnection
from src.app.database.postgres_db import PostgresConnection

load_dotenv()

mongo = MongoDBConnection(os.getenv("MONGO_URI"))
postgres = PostgresConnection(os.getenv("POSTGRES_URI"))

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
