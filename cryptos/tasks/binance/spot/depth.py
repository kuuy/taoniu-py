from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.models.binance.spot.symbol import Symbol
from cryptos.repositories.binance.spot import depth as repository

@celery.task(ignore_result=True)
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    sync.delay(symbol)

@celery.task(time_limit=5, ignore_result=True)
def sync(symbol):
  lock = redis.lock(
    'locks:binance:spot:depth:sync:{}'.format(symbol),
    timeout=5,
  )
  try:
    if not lock.acquire():
      return
    repository.sync(symbol)
  except:
    pass
  finally:
    lock.release()