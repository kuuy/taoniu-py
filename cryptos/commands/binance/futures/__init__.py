from flask import Blueprint

bp = Blueprint('futures', __name__)

def register_blueprint():
  from . import (
    rules,
    websocket,
  )
  bp.register_blueprint(rules.bp)
  bp.register_blueprint(websocket.bp)

