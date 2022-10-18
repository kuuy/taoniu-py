from flask import Blueprint

bp = Blueprint('spot', __name__)

def register_blueprint():
  from . import(
    klines,
    schedules,
  )
  klines.register_blueprint()
  bp.register_blueprint(klines.bp)
  bp.register_blueprint(schedules.bp)
