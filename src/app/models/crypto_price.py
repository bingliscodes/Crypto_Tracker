from sqlalchemy import Column, String, Float, DateTime
from src.app.database.postgres_db import Base
from datetime import datetime, timezone
from uuid import uuid4


class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
