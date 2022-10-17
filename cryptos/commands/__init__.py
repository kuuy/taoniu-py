def register_blueprint(app):
  from . import (
    ai,
    binance,
    tradingview,
  )
  ai.register_blueprint()
  binance.register_blueprint()
  tradingview.register_blueprint()

  app.register_blueprint(ai.bp)
  app.register_blueprint(binance.bp)
  app.register_blueprint(tradingview.bp)
