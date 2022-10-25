from binance import Client
from xid import Xid

from cryptos import db
from cryptos.config.binance import spot as config
from cryptos.models.binance.spot.kline import Kline1d

def sync(symbol, limit):
  client = Client(api_key=config.KLINES_API_KEY, api_secret=config.KLINES_SECRET_KEY)
  klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=limit)
  for kline in klines:
    timestamp = kline[0]
    entity = db.session.query(Kline1d).filter_by(
      symbol=symbol,
      timestamp=timestamp,
    ).first()
    if entity is None:
      entity = Kline1d(
        id=Xid().string(),
        symbol=symbol,
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
