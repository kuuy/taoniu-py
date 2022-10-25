
def autodiscover_tasks():
  from . import spot
  autodiscover_tasks = [
    'cryptos.tasks.binance.spot.tickers'
  ]
  autodiscover_tasks += spot.autodiscover_tasks()
  return autodiscover_tasks
