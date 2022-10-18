from flask import Blueprint

bp = Blueprint('klines', __name__)

def register_blueprint():
  from . import daily
  bp.register_blueprint(daily.bp)
