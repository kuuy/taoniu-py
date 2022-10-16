from datetime import datetime

from tradingview_ta import get_multiple_analysis
from xid import Xid

from cryptos import db
from cryptos.models.tradingview.analysis import Analysis


def scan(symbols, interval):
  analysis = get_multiple_analysis(
    'CRYPTO', interval, symbols
  )
  for symbol, item in analysis.items():
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

  db.session.commit()
