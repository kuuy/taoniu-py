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
  port = redis.srandmember('proxies:tor:online')
  if port is None:
    return
  proxy = 'socks5://127.0.0.1:{}'.format(port)
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
  except requests.exceptions.ConnectionError:
    redis.srem('proxies:tor:online', port)
    redis.sadd('proxies:tor:offline', port)
  except BinanceAPIException as e:
    if 'IP banned' in e.message:
      redis.srem('proxies:tor:online', port)
      redis.sadd('proxies:tor:offline', port)
    else:
      redis.zincrby('proxies:tor:failed', 1, port)
  except:
    redis.zincrby('proxies:tor:failed', 1, port)

