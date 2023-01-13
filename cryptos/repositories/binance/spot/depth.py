import time
import json

import requests

from binance import Client
from binance.exceptions import BinanceAPIException

from cryptos import (
  db,
  redis,
)
from cryptos.models.binance.spot.symbol import Symbol

def sync(symbol):
  proxy = 'socks5://127.0.0.1:1088'
  proxies = {
    'http': proxy,
    'https': proxy
  }
  try:
    client = Client(
      requests_params={
        'proxies': proxies,
        'timeout': 3,
      },
    )
    data = client.get_order_book(symbol=symbol, limit=1000)
    entity = db.session.query(Symbol).filter_by(
      symbol=symbol,
    ).first()
    if entity is not None:
      entity.depth = data
      db.session.add(entity)
      db.session.commit()
  except:
    pass

