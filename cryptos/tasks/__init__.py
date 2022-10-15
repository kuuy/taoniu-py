from celery import Celery
from kombu import Queue

def make_celery(app):
  celery = Celery(
    app.import_name,
    broker=app.config['broker_url'],
    backend=app.config['result_backend'],
    fixups=[],
  )
  celery.conf.task_queues = (
    Queue(
      'cryptos.binance.futures',
      routing_key='cryptos.tasks.binance.futures.#'
    ),
    Queue(
      'cryptos.binance.spot',
      routing_key='cryptos.tasks.binance.spot.#'
    ),
    Queue(
      'cryptos.tradingview',
      routing_key='cryptos.tasks.tradingview.#'
    ),
  )
  celery.autodiscover_tasks([
    'cryptos.tasks.binance.futures.realtime',
  ])
  celery.conf.update(app.config)

  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
       return self.run(*args, **kwargs)

  celery.Task = ContextTask

  return celery

