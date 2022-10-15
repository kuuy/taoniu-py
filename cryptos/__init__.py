import sys
import click

from flask import Flask
from flask.cli import FlaskGroup
from flask_redis import Redis

from cryptos.tasks import make_celery

def create_app():
  app = Flask(__name__)
  app.config['REDIS_URL'] = 'redis://localhost:6379/8'
  app.config['REDIS_DECODE_RESPONSES'] = True
  app.config.update(
    broker_url='redis://localhost:6379/11',
    result_backend='redis://localhost:6379/11'
  )

  from . import commands
  commands.register_blueprint(app)

  redis.init_app(app)

  return app

def make_app():
  return app

@click.group(cls=FlaskGroup, create_app=make_app)
def cli():
  """Management script for the Cryptos"""

redis = Redis()
app = create_app()
celery = make_celery(app)
