def autodiscover_tasks():
  from . import binance
  autodiscover_tasks = []
  autodiscover_tasks += binance.autodiscover_tasks()
  return autodiscover_tasks