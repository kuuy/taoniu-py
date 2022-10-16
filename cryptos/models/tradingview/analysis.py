from sqlalchemy import (
  func,
  Column,
  String,
  Integer,
  DateTime,
  JSON,
  UniqueConstraint,
)

from cryptos import db

class Analysis(db.Model):
  id = Column(String(20), primary_key=True)
  exchange = Column(String(20), nullable=False)
  symbol = Column(String(20), nullable=False)
  interval = Column(String(20), nullable=False)
  oscillators = Column(JSON, nullable=False)
  moving_averages = Column(JSON, nullable=False)
  indicators = Column(JSON, nullable=False)
  summary = Column(JSON, nullable=False)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

  UniqueConstraint(
    "exchange",
    "symbol",
    "interval",
    name="unq_tradingview_cryptos_analysis_exchange_symbol_interval",
  ),

  __tablename__ = "tradingview_cryptos_analysis"
