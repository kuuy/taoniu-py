from datetime import (
  datetime,
  timedelta,
)

from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.models.binance.symbol import Symbol
from cryptos.models.binance.spot.kline import Kline1d
from cryptos.repositories.binance.spot.klines import daily as repository

@celery.task(ignore_result=True)
def flush(limit):
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    sync.delay(symbol, limit)

@celery.task(ignore_result=True)
def fix():
  now = datetime.now() + timedelta(minutes=-10)
  offset = now.astimezone().utcoffset().total_seconds()
  utc = now + timedelta(seconds=-offset)
  duration = timedelta(hours=8 - utc.hour, minutes=-utc.minute, seconds=-utc.second, microseconds=-utc.microsecond)
  opentime = int((utc + duration).timestamp() * 1000)

  exists = []
  klines = db.session.query(
    Kline1d.symbol,
    Kline1d.timestamp,
    Kline1d.updated_at,
  ).filter(
    Kline1d.timestamp == opentime,
  ).all()
  for kline in klines:
    delay = now - kline.updated_at.replace(tzinfo=None)
    if delay.total_seconds() > 300:
      sync.delay(kline.symbol, 1)
    exists.append(kline.symbol)

  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for symbol in symbols:
    if symbol not in exists:
      sync.delay(symbol, 1)

@celery.task(time_limit=5, ignore_result=True)
def sync(symbol, limit):
  lock = redis.lock(
    'locks:binance:spot:klines:daily:sync:{}:{}'.format(
      symbol,
      limit,
    ),
    timeout=5,
  )
  try:
    if not lock.acquire():
      return
    repository.sync(symbol, limit)
  except:
    pass
  finally:
    lock.release()