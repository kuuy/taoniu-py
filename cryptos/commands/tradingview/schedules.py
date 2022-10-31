import celery
from flask import Blueprint, current_app
from redbeat import RedBeatSchedulerEntry

import cryptos

bp = Blueprint('schedules', __name__)

@bp.cli.command()
def apply():
  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-1m',
    'cryptos.tasks.tradingview.binance.scanner.flush',
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
    'tradingview-binance-scanner-fix-1m',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['1m', 1],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=120)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-5m',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['5m'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=30)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-5m',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['5m', 2],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=180)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-15m',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['15m'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=45)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-15m',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['15m', 3],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-30m',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['30m'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-30m',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['30m', 5],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-1h',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['1h'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-1h',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['1h', 5],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-2h',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['2h'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-2h',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['2h', 5],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-4h',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['4h'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-4h',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['4h', 5],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=300)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-1d',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    interval,
    args=['1d'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  interval = celery.schedules.schedule(run_every=60)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-1d',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    interval,
    args=['1d', 5],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  crontab = celery.schedules.crontab(hour='*/3')
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-1W',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    crontab,
    args=['1W'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  crontab = celery.schedules.crontab(minute=45)
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-1W',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    crontab,
    args=['1W', 180],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  crontab = celery.schedules.crontab(hour='*/12')
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-flush-1M',
    'cryptos.tasks.tradingview.binance.scanner.flush',
    crontab,
    args=['1M'],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()

  crontab = celery.schedules.crontab(hour='*/3')
  entry = RedBeatSchedulerEntry(
    'tradingview-binance-scanner-fix-1M',
    'cryptos.tasks.tradingview.binance.scanner.fix',
    crontab,
    args=['1M', 720],
    app=cryptos.celery
  )
  try:
    entry.load_definition(entry.key)
  except KeyError:
    entry.save()