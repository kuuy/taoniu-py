import requests

from binance import Client
from binance.exceptions import BinanceAPIException
from xid import Xid

from cryptos import (
  db,
  redis,
)
from cryptos.models.binance.spot.kline import Kline

def sync(symbol, interval, limit):
  proxy = 'socks5://127.0.0.1:1088'
  proxies = {
    'http': proxy,
    'https': proxy
  }
  try:
    client = Client(
      requests_params={
        'proxies': proxies,
        'timeout': 5,
      },
    )
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    for kline in klines:
      timestamp = kline[0]
      entity = db.session.query(Kline).filter_by(
        symbol=symbol,
        interval=interval,
        timestamp=timestamp,
      ).first()
      if entity is None:
        entity = Kline(
          id=Xid().string(),
          symbol=symbol,
          interval=interval,
          open=float(kline[1]),
          close=float(kline[4]),
          high=float(kline[2]),
          low=float(kline[3]),
          volume=float(kline[5]),
          quota=float(kline[7]),
          timestamp=float(kline[0]),
        )
      else:
        entity.open = float(kline[1])
        entity.close = float(kline[4])
        entity.high = float(kline[2])
        entity.low = float(kline[3])
        entity.volume = float(kline[5])
        entity.quota = float(kline[7])

      db.session.add(entity)

    db.session.commit()
  except:
    pass
