import hashlib

from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.tradingview import scanner as repository

@celery.task(ignore_result=True)
def flush(interval):
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for i in range(0, len(symbols), 50):
    scan.delay(symbols[i:i + 50], interval)

@celery.task(time_limit=5, ignore_result=True)
def scan(symbols, interval):
  lock = redis.lock(
    'locks:tradingview:scanner:scan:{}'.format(
      hashlib.md5(
        '{}:{}'.format(
          ','.join(symbols),
          interval,
        ).encode('ascii')
      ),
    ),
    timeout=5,
  )
  try:
    if not lock.acquire():
      return
    repository.scan(symbols, interval)
  except:
    pass
  finally:
    lock.release()
