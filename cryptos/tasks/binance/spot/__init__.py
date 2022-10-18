def autodiscover_tasks():
  from . import klines
  autodiscover_tasks = []
  autodiscover_tasks += klines.autodiscover_tasks()
  return autodiscover_tasks