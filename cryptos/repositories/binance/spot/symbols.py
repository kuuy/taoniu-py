from cryptos import db
from cryptos.models.binance.spot.symbol import Symbol

def symbols():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]

  return symbols
