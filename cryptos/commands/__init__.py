def register_blueprint(app):
  from . import binance
  binance.register_blueprint()

  app.register_blueprint(binance.bp)
