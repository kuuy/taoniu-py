import hashlib

from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.binance.spot import tickers as repository

@celery.task(ignore_result=True)
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for i in range(0, len(symbols), 20):
    sync.delay(symbols[i:i + 20])

@celery.task(time_limit=5, ignore_result=True)
def sync(symbols):
  lock = redis.lock(
    'locks:binance:spot:tickers:sync:{}'.format(
      hashlib.md5(','.join(symbols).encode('ascii')),
    ),
    timeout=5,
  )
  try:
    if not lock.acquire():
      return
    repository.sync(symbols)
  except:
    pass
  finally:
    lock.release()