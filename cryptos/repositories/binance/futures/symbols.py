from cryptos import db
from cryptos.models.binance.futures.symbol import Symbol

def symbols():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.status == 'TRADING',
  ).all()]

  return symbols
