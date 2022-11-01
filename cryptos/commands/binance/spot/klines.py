from datetime import (
  datetime,
  timedelta,
)

import click
from flask import Blueprint

from cryptos import db
from cryptos.models.binance.spot.symbol import Symbol
from cryptos.models.binance.spot.kline import Kline
from cryptos.repositories.binance.spot import klines as repository

bp = Blueprint('klines', __name__)

@bp.cli.command()
@click.argument('interval', nargs=1)
@click.argument('limit', type=int)
def flush(interval, limit):
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    repository.sync(symbol, interval, limit)

@bp.cli.command()
@click.argument('interval', nargs=1)
def fix(interval):
  now = datetime.now()+timedelta(minutes=-5)
  offset = now.astimezone().utcoffset().total_seconds()
  utc = now + timedelta(seconds=-offset)
  duration = timedelta(hours=8-utc.hour, minutes=-utc.minute, seconds=-utc.second, microseconds=-utc.microsecond)
  opentime = int((utc + duration).timestamp() * 1000)

  exists = []
  klines = db.session.query(
    Kline.symbol,
    Kline.timestamp,
    Kline.updated_at,
  ).filter(
    Kline.interval == interval,
    Kline.timestamp == opentime,
  ).all()
  for kline in klines:
    delay = now - kline.updated_at.replace(tzinfo=None)
    if delay.total_seconds() > 300:
      repository.sync(kline.symbol, interval, 1)
    exists.append(kline.symbol)

  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    if symbol not in exists:
      repository.sync(kline.symbol, interval, 1)
