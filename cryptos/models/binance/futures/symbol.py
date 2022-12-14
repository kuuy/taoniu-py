from sqlalchemy import (
  String,
  JSON,
  Column,
  DateTime,
  func,
)

from cryptos import db

class Symbol(db.Model):
  id = Column(String(20), primary_key=True)
  symbol = Column(String(20), nullable=False, unique=True)
  base_asset = Column(String(20), nullable=False)
  quote_asset = Column(String(20), nullable=False)
  filters = Column(JSON, nullable=False)
  status = Column(String(20), nullable=False)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

  __tablename__ = 'binance_futures_symbols'