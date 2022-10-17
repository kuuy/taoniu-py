import click

from flask import Flask
from flask.cli import FlaskGroup
from flask_redis import Redis
from flask_sqlalchemy import SQLAlchemy

from cryptos import models
from cryptos.tasks import make_celery

def create_app():
  app = Flask(__name__)
  app.config['TIMEZONE'] = "Asia/Shanghai"
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://taoniu:64EQJMn1O9JrZ2G4@localhost/taoniu"
  app.config['REDIS_URL'] = 'redis://localhost:6379/8'
  app.config['REDIS_DECODE_RESPONSES'] = True
  app.config.update(
    redbeat_redis_url='redis://localhost:6379/11',
    broker_url='redis://localhost:6379/11',
    result_backend='redis://localhost:6379/11',
  )

  from . import commands
  commands.register_blueprint(app)

  db.init_app(app)
  redis.init_app(app)

  return app

def make_app():
  return app

@click.group(cls=FlaskGroup, create_app=make_app)
def cli():
  """Management script for the Cryptos"""

db = SQLAlchemy()
redis = Redis()
app = create_app()
celery = make_celery(app)