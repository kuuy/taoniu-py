from flask import Blueprint

bp = Blueprint('binance', __name__)

def register_blueprint():
  from . import scanner
  bp.register_blueprint(scanner.bp)
