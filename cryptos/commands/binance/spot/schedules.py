import celery
from flask import Blueprint, current_app
from redbeat import RedBeatSchedulerEntry

import cryptos

bp = Blueprint('schedules', __name__)

@bp.cli.command()
def apply():
  interval = celery.schedules.schedule(run_every=5)
  entry = RedBeatSchedulerEntry(
    'binance-spot-tickers-flush',
    'cryptos.tasks.binance.spot.tickers.flush',
    interval,
    args=[],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'binance-spot-klines-daily-flush-5m',
    'cryptos.tasks.binance.spot.klines.daily.flush',
    interval,
    args=[1],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  crontab = celery.schedules.crontab(minute=30, hour=0)
  entry = RedBeatSchedulerEntry(
    'binance-spot-klines-daily-flush',
    'cryptos.tasks.binance.spot.klines.daily.flush',
    crontab,
    args=[5],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()