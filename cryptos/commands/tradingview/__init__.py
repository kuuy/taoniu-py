from flask import Blueprint

bp = Blueprint('tradingview', __name__)

def register_blueprint():
  from . import (
    binance,
    schedules,
  )
  binance.register_blueprint()
  bp.register_blueprint(binance.bp)
  bp.register_blueprint(schedules.bp)
