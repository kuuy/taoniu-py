from flask import Blueprint

from cryptos import db
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.binance.spot import tickers as repository

bp = Blueprint('tickers', __name__)

@bp.cli.command()
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for i in range(0, len(symbols), 20):
    repository.sync(symbols[i:i + 20])
