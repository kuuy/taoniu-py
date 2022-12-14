from celery import Celery

from cryptos.tasks import (
  binance,
  tradingview,
)

def make_celery(app):
  celery = Celery(
    app.import_name,
    broker=app.config['broker_url'],
    backend=app.config['result_backend'],
    fixups=[],
  )
  celery.conf.task_routes = {
    'cryptos.tasks.binance.spot.tickers.*': {
      'queue': 'cryptos.tasks.binance.spot.tickers',
    },
    'cryptos.tasks.binance.spot.depth.*': {
      'queue': 'cryptos.tasks.binance.spot.depth',
    },
    'cryptos.tasks.binance.spot.klines.*': {
      'queue': 'cryptos.tasks.binance.spot.klines',
    },
    'cryptos.tasks.binance.futures.tickers.*': {
      'queue': 'cryptos.tasks.binance.futures.tickers',
    },
    'cryptos.tasks.binance.futures.klines.*': {
      'queue': 'cryptos.tasks.binance.futures.klines',
    },
    'cryptos.tasks.tradingview.*': {
      'queue': 'cryptos.tasks.tradingview',
    },
  }
  autodiscover_tasks = []
  autodiscover_tasks += binance.autodiscover_tasks()
  autodiscover_tasks += tradingview.autodiscover_tasks()
  celery.autodiscover_tasks(autodiscover_tasks)
  celery.conf.update(app.config)

  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
       return self.run(*args, **kwargs)

  celery.Task = ContextTask

  return celery

