from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
from src.app.database.mongo_db import MongoDBConnection

mongo_connection = MongoDBConnection(os.getenv("MONGO_DB_URI"))

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
