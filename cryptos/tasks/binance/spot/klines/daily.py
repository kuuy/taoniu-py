from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.binance.spot.klines import daily as repository

@celery.task(ignore_result=True)
def flush(limit):
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter_by(status='TRADING').all()]
  for symbol in symbols:
    sync.delay(symbol, limit)

@celery.task(time_limit=5, ignore_result=True)
def sync(symbol, limit):
  lock = redis.lock(
    'locks:binance:spot:klines:daily:sync:{}:{}'.format(
      symbol,
      limit,
    ),
    timeout=10,
  )
  try:
    if not lock.acquire():
      return
    repository.sync(symbol, limit)
  except:
    pass
  finally:
    lock.release()