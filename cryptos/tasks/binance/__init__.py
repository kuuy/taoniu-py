
def autodiscover_tasks():
  from . import (
    spot,
    futures,
  )
  autodiscover_tasks = []
  autodiscover_tasks += spot.autodiscover_tasks()
  autodiscover_tasks += futures.autodiscover_tasks()
  return autodiscover_tasks
