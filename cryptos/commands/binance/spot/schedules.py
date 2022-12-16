import celery
from flask import Blueprint, current_app
from redbeat import RedBeatSchedulerEntry

import cryptos

bp = Blueprint('schedules', __name__)

@bp.cli.command()
def apply():
  interval = celery.schedules.schedule(run_every=30)
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
    'binance-spot-depth-flush',
    'cryptos.tasks.binance.spot.depth.flush',
    interval,
    args=[],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=15)
  entry = RedBeatSchedulerEntry(
    'binance-spot-tickers-fix',
    'cryptos.tasks.binance.spot.tickers.fix',
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
    'binance-spot-klines-flush-1d',
    'cryptos.tasks.binance.spot.klines.flush',
    interval,
    args=['1d', 1],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'binance-spot-klines-fix-1d',
    'cryptos.tasks.binance.spot.klines.fix',
    interval,
    args=['1d', 1],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()
