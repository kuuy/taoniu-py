import time

from flask import Blueprint

from cryptos import (
  db,
  redis,
)
from cryptos.models.binance.spot.symbol import Symbol
from cryptos.repositories.binance.spot import depth as repository

bp = Blueprint('depth', __name__)

@bp.cli.command()
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    repository.sync(symbol)
    break
