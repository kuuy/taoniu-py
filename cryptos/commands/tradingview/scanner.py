from flask import Blueprint

import cryptos
from cryptos import db
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.tradingview import scanner as repository

bp = Blueprint('scanner', __name__)

@bp.cli.command()
def flush():
  symbols = ['BINANCE:{}'.format(x[0]) for x in db.session.query(Symbol.symbol).filter_by(status='TRADING').all()]
  for i in range(0, len(symbols), 50):
    repository.scan(symbols[i:i + 50], '1m')

@bp.cli.command()
def test():
  from cryptos.tasks.tradingview import scanner as task
  task.flush.delay('1m')