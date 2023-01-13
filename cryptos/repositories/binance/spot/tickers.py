import time
import json

import requests

from binance import Client
from binance.exceptions import BinanceAPIException

from cryptos import redis

def sync(symbols):
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
    tickers = client.get_ticker(symbols=json.dumps(symbols, separators=(',', ':')))
    timestamp = int(time.time())
    with redis.pipeline() as pipe:
      for item in tickers:
        redisKey = 'binance:spot:realtime:{}'.format(item['symbol'])
        lasttime = int(redis.hget(redisKey, 'timestamp') or 0)
        if lasttime >= timestamp:
          continue
        pipe.hmset(
          redisKey,
          dict(
            symbol=item['symbol'],
            open=float(item['openPrice']),
            price=float(item['lastPrice']),
            high=float(item['highPrice']),
            low=float(item['lowPrice']),
            volume=float(item['volume']),
            quota=float(item['quoteVolume']),
            timestamp=timestamp,
          ),
        )
      pipe.execute()
  except:
    pass

