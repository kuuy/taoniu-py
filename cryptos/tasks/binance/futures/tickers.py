import time
import hashlib

from cryptos import (
  db,
  redis,
  celery,
)
from cryptos.models.binance.futures.symbol import Symbol
from cryptos.repositories.binance.futures import tickers as repository

@celery.task(ignore_result=True)
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.status == 'TRADING',
  ).all()]
  for i in range(0, len(symbols), 20):
    sync.delay(symbols[i:i + 20])

@celery.task(ignore_result=True)
def fix():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.status == 'TRADING',
  ).all()]
  fields = [
    'timestamp'
  ]
  lua_script = '''
  local hmget = function (key)
    local hash = {}
    local data = redis.call('HMGET', key, unpack(ARGV))
    for i = 1, #ARGV do
      hash[i] = data[i]
    end
    return hash
  end
  local data = {}
  for i = 1, #KEYS do
    local key = 'binance:futures:realtime:' .. KEYS[i]
    if redis.call('EXISTS', key) == 0 then
      data[i] = false
    else
      data[i] = hmget(key)
    end
  end
  return data
  '''
  cmd = redis.register_script(lua_script)
  result = cmd(keys=symbols, args=fields)
  timestamp = int(time.time())
  items = []
  for i in range(len(symbols)):
    if result[i] is None:
      items.append(symbols[i])
      continue
    data = {}
    for j in range(len(fields)):
      data[fields[j]] = result[i][j]
    if timestamp - int(data['timestamp']) > 30:
      items.append(symbols[i])

  for i in range(0, len(items), 20):
    sync.delay(items[i:i + 20])

@celery.task(time_limit=5, ignore_result=True)
def sync(symbols):
  lock = redis.lock(
    'locks:binance:futures:tickers:sync:{}'.format(
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