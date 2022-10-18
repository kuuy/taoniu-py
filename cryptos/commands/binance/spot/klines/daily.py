from flask import Blueprint

from cryptos import db
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.binance.spot.klines import daily as repository

bp = Blueprint('daily', __name__)

@bp.cli.command()
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter_by(status='TRADING').all()]
  for symbol in symbols:
    repository.sync(symbol, 100)
