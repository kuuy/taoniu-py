def register_blueprint(app):
  from . import (
    binance,
    tradingview,
  )
  binance.register_blueprint()
  tradingview.register_blueprint()

  app.register_blueprint(binance.bp)
  app.register_blueprint(tradingview.bp)
