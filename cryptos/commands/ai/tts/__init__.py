from flask import Blueprint

bp = Blueprint('tts', __name__)

def register_blueprint():
  from . import (
    tacotron2,
  )
  bp.register_blueprint(tacotron2.bp)
