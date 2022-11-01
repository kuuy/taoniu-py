from flask import Blueprint

bp = Blueprint('futures', __name__)

def register_blueprint():
  from . import (
    klines,
    tickers,
    schedules,
  )
  bp.register_blueprint(klines.bp)
  bp.register_blueprint(tickers.bp)
  bp.register_blueprint(schedules.bp)
