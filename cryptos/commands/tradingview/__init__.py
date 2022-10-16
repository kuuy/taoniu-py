from flask import Blueprint

bp = Blueprint('tradingview', __name__)

def register_blueprint():
  from . import (
    scanner,
    schedules,
  )
  bp.register_blueprint(scanner.bp)
  bp.register_blueprint(schedules.bp)
