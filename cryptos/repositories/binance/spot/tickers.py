import time
import json

from binance import Client

from cryptos import redis
from cryptos.config.binance import spot as config

def sync(symbols):
  client = Client(api_key=config.TICKERS_API_KEY, api_secret=config.TICKERS_SECRET_KEY)
  tickers = client.get_ticker(symbols=json.dumps(symbols, separators=(',', ':')))
  timestamp = int(time.time())
  with redis.pipeline() as pipe:
    for item in tickers:
      redisKey = 'binance:spot:realtime:{}'.format(item['symbol'])
      lasttime = int(redis.hget(redisKey, 'timestamp') or 0)
      if lasttime > timestamp:
        continue
      pipe.hmset(
        redisKey,
        dict(
          symbol=item['symbol'],
          price=float(item['lastPrice']),
          open=float(item['openPrice']),
          high=float(item['highPrice']),
          low=float(item['lowPrice']),
          volume=float(item['volume']),
          quota=float(item['quoteVolume']),
          timestamp=timestamp,
        ),
      )
    pipe.execute()
