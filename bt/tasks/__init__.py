from celery import Celery

def make_celery(app):
  celery = Celery(
    app.import_name,
    broker=app.config['broker_url'],
    backend=app.config['result_backend'],
    fixups=[],
  )
  celery.conf.task_routes = {}
  autodiscover_tasks = []
  celery.autodiscover_tasks(autodiscover_tasks)
  celery.conf.update(app.config)

  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
       return self.run(*args, **kwargs)

  celery.Task = ContextTask

  return celery

