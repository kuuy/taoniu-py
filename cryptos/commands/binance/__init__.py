from flask import Blueprint

bp = Blueprint('binance', __name__)

def register_blueprint():
    from . import futures
    futures.register_blueprint()
    bp.register_blueprint(futures.bp)
