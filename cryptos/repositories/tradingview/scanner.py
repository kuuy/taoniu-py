from datetime import datetime

from tradingview_ta import get_multiple_analysis
from xid import Xid

from cryptos import (
  db,
  redis,
)
from cryptos.models.tradingview.analysis import Analysis

def scan(symbols, interval, is_proxy=True):
  if is_proxy:
    port = redis.srandmember('proxies:tor:online')
    if port is None:
      return
    proxy = 'socks5://127.0.0.1:{}'.format(port)
    proxies = {
      'http': proxy,
      'https': proxy
    }
  else:
    proxies = None
  try:
    analysis = get_multiple_analysis(
      'CRYPTO',
      interval,
      symbols,
      timeout=10,
      proxies=proxies,
    )
    for symbol, item in analysis.items():
      if item is None:
        continue

      entity = db.session.query(Analysis).filter_by(
        exchange=item.exchange,
        symbol=item.symbol,
        interval=item.interval,
      ).first()
      if entity is None:
        entity = Analysis(
          id=Xid().string(),
          exchange=item.exchange,
          symbol=item.symbol,
          interval=item.interval,
          oscillators=item.oscillators,
          moving_averages=item.moving_averages,
          indicators=item.indicators,
          summary=item.summary,
        )
      else:
        entity.oscillators = item.oscillators
        entity.moving_averages = item.moving_averages
        entity.indicators = item.indicators
        entity.summary = item.summary

      db.session.add(entity)

      redis.zrem('tradingview:analysis:flush:1m', item.symbol)

    db.session.commit()
  except:
    redis.zincrby('proxies:tor:failed', 1, port)
