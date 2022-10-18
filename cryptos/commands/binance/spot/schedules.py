import celery
from flask import Blueprint, current_app
from redbeat import RedBeatSchedulerEntry

import cryptos

bp = Blueprint('schedules', __name__)

@bp.cli.command()
def apply():
  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'binance-spot-klines-daily-flush-5m',
    'cryptos.tasks.binance.spot.klines.flush',
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
    'cryptos.tasks.binance.spot.klines.flush',
    crontab,
    args=[2],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()