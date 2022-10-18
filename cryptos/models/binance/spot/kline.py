from sqlalchemy import (
  String,
  Integer,
  Float,
  Column,
  DateTime,
  func,
  UniqueConstraint,
)

from cryptos import db

class Kline1d(db.Model):
  id = Column(String(20), primary_key=True)
  symbol = Column(String(20), nullable=False, unique=True)
  open = Column(Float, nullable=False)
  close = Column(Float, nullable=False)
  high = Column(Float, nullable=False)
  low = Column(Float, nullable=False)
  volume = Column(Float, nullable=False)
  quota = Column(Float, nullable=False)
  timestamp = Column(Integer, nullable=False)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

  UniqueConstraint(
    "symbol",
    "timestamp",
    name="unq_binance_spot_klines_1d_symbol_timestamp",
  ),

  __tablename__ = "binance_spot_klines_1d"
