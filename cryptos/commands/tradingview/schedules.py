import celery
from flask import Blueprint, current_app
from redbeat import RedBeatSchedulerEntry

import cryptos

bp = Blueprint('schedules', __name__)

@bp.cli.command()
def apply():
  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-scanner-flush',
    'cryptos.tasks.tradingview.scanner.flush',
    interval,
    args=['1m'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=15)
  entry = RedBeatSchedulerEntry(
    'tradingview-scanner-fix-binance-1m',
    'cryptos.tasks.tradingview.scanner.fix',
    interval,
    args=['BINANCE', '1m', 1],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()
