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
from cryptos.models.tradingview.analysis import Analysis
from cryptos.repositories.binance.spot.symbols import symbols as spot_symbols
from cryptos.repositories.binance.futures.symbols import symbols as futures_symbols
from cryptos.repositories.tradingview import scanner as repository

@celery.task(ignore_result=True)
def flush(interval):
  symbols = spot_symbols() + futures_symbols()
  for i in range(0, len(symbols), 50):
    scan.delay(['BINANCE:{}'.format(x) for x in symbols[i:i + 50]], interval)

@celery.task(ignore_result=True)
def fix(interval, delay):
  symbols = spot_symbols() + futures_symbols()

  starttime = datetime.now() - timedelta(minutes=delay)
  exists = [x[0] for x in db.session.query(
    Analysis.symbol,
  ).filter(
    Analysis.exchange == 'BINANCE',
    Analysis.interval == interval,
    Analysis.updated_at > starttime,
  ).all()]

  items = []
  for symbol in symbols:
    if symbol in exists:
      continue
    items.append(symbol)

  for i in range(0, len(items), 50):
    scan.delay(['BINANCE:{}'.format(x) for x in items[i:i + 50]], interval)

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
    timeout=10,
  )
  try:
    if not lock.acquire():
      return
    repository.scan(symbols, interval)
  except:
    pass
  finally:
    lock.release()
