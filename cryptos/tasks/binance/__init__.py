
def autodiscover_tasks():
  from . import spot
  autodiscover_tasks = []
  autodiscover_tasks += spot.autodiscover_tasks()
  return autodiscover_tasks
