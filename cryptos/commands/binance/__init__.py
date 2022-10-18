from flask import Blueprint

bp = Blueprint('binance', __name__)

def register_blueprint():
  from . import (
    spot,
    futures,
  )
  spot.register_blueprint()
  futures.register_blueprint()
  bp.register_blueprint(spot.bp)
  bp.register_blueprint(futures.bp)
