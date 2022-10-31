from datetime import (
  datetime,
  timedelta,
)

from flask import Blueprint

from cryptos import db
from cryptos.models.binance.symbol import Symbol
from cryptos.models.tradingview.analysis import Analysis
from cryptos.repositories.tradingview import scanner as repository

bp = Blueprint('scanner', __name__)

@bp.cli.command()
def flush():
  symbols = ['BINANCE:{}'.format(x[0]) for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for i in range(0, len(symbols), 50):
    repository.scan(symbols[i:i + 50], '1m')

@bp.cli.command()
def fix():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]

  starttime = datetime.now() - timedelta(minutes=1)
  exists = [x[0] for x in db.session.query(
    Analysis.symbol,
  ).filter(
    Analysis.exchange == 'BINANCE',
    Analysis.interval == '1m',
    Analysis.updated_at > starttime,
  ).all()]

  items = []
  for symbol in symbols:
    if symbol in exists:
      continue
    items.append(symbol)

  for i in range(0, len(items), 50):
    repository.scan(['BINANCE:{}'.format(x) for x in items[i:i + 50]], '1m')
