import hashlib

from datetime import (
  datetime,
  timedelta,
)

from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.repositories.binance.spot.symbols import symbols as spot_symbols
from cryptos.repositories.tradingview import scanner as repository

@celery.task(ignore_result=True)
def flush(interval):
  symbols = spot_symbols()
  for i in range(0, len(symbols), 50):
    scan.delay(['BINANCE:{}'.format(x) for x in symbols[i:i + 50]], interval)

@celery.task(ignore_result=True)
def fix(interval):
  symbols = redis.zrevrange(
    'tradingview:analysis:flush:{}'.format(interval),
    0,
    -1,
  )
  for i in range(0, len(symbols), 20):
    scan.delay(['BINANCE:{}'.format(x) for x in symbols[i:i + 20]], interval, False)

@celery.task(time_limit=5, ignore_result=True)
def scan(symbols, interval, is_proxy=False):
  lock = redis.lock(
    'locks:tradingview:scanner:scan:{}'.format(
      hashlib.md5(
        '{}:{}'.format(
          ','.join(symbols),
          interval,
        ).encode('ascii')
      ),
    ),
    timeout=10,
  )
  try:
    if not lock.acquire():
      return
    repository.scan(symbols, interval, is_proxy)
  except:
    pass
  finally:
    lock.release()
