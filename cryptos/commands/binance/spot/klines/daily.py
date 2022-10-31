from datetime import (
  datetime,
  timedelta,
)

from flask import Blueprint

from cryptos import db
from cryptos.models.binance.symbol import Symbol
from cryptos.models.binance.spot.kline import Kline1d
from cryptos.repositories.binance.spot.klines import daily as repository

bp = Blueprint('daily', __name__)

@bp.cli.command()
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    repository.sync(symbol, 100)

@bp.cli.command()
def fix():
  now = datetime.now()+timedelta(minutes=-5)
  offset = now.astimezone().utcoffset().total_seconds()
  utc = now + timedelta(seconds=-offset)
  duration = timedelta(hours=8-utc.hour, minutes=-utc.minute, seconds=-utc.second, microseconds=-utc.microsecond)
  opentime = int((utc + duration).timestamp() * 1000)

  exists = []
  klines = db.session.query(
    Kline1d.symbol,
    Kline1d.timestamp,
    Kline1d.updated_at,
  ).filter(
    Kline1d.timestamp == opentime,
  ).all()
  for kline in klines:
    delay = now - kline.updated_at.replace(tzinfo=None)
    if delay.total_seconds() > 300:
      repository.sync(kline.symbol, 1)
    exists.append(kline.symbol)

  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    if symbol not in exists:
      repository.sync(kline.symbol, 1)
