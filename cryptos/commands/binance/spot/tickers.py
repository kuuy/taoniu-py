import time

from flask import Blueprint

from cryptos import (
  db,
  redis,
)
from cryptos.models.binance.symbol import Symbol
from cryptos.repositories.binance.spot import tickers as repository

bp = Blueprint('tickers', __name__)

@bp.cli.command()
def flush():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
    Symbol.status == 'TRADING',
  ).all()]
  for i in range(0, len(symbols), 20):
    repository.sync(symbols[i:i + 20])
    break

@bp.cli.command()
def fix():
  symbols = [x[0] for x in db.session.query(Symbol.symbol).filter(
    Symbol.is_spot,
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
    local key = 'binance:spot:realtime:' .. KEYS[i]
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
    repository.sync(items[i:i + 20])
