def register_blueprint(app):
  from . import (
    peers,
  )

  app.register_blueprint(peers.bp)
