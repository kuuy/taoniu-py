from flask import Blueprint

bp = Blueprint('spot', __name__)

def register_blueprint():
  from . import(
    tickers,
    depth,
    klines,
    schedules,
  )
  bp.register_blueprint(tickers.bp)
  bp.register_blueprint(depth.bp)
  bp.register_blueprint(klines.bp)
  bp.register_blueprint(schedules.bp)
