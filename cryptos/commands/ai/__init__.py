from flask import Blueprint

bp = Blueprint('ai', __name__)

def register_blueprint():
    from . import tts
    tts.register_blueprint()
    bp.register_blueprint(tts.bp)
