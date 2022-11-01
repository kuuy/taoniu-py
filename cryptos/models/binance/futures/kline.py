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

class Kline(db.Model):
  id = Column(String(20), primary_key=True)
  symbol = Column(String(20), nullable=False)
  interval = Column(String(20), nullable=False)
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
    'symbol',
    'interval',
    'timestamp',
    name='unq_binance_futures_klines_symbol_interval_timestamp',
  ),

  __tablename__ = 'binance_futures_klines'
