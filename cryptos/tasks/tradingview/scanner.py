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
  symbols = ['BINANCE:{}'.format(x[0]) for x in db.session.query(Symbol.symbol).filter_by(status='TRADING').all()]
  for i in range(0, len(symbols), 50):
    scan.delay(symbols[i:i + 50], interval)

@celery.task(exchange='cryptos:tradingview', time_limit=5, ignore_result=True)
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
    timeout=10,
  )
  try:
    if not lock.acquire():
      return
    repository.scan(symbols, interval)
  finally:
    lock.release()
