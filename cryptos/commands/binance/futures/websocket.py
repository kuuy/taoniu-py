import asyncio

from binance import (
  AsyncClient,
  BinanceSocketManager,
)
from binance.exceptions import BinanceAPIException

from flask import Blueprint

bp = Blueprint('websocket', __name__)

async def multiplex_socket(bm):
  print(bm.__dict__)
  async with bm.multiplex_socket([
    'ethusdt@miniTicker',
  ]) as stream:
    while True:
      print(1)
      res = await stream.recv()
      print(res)

async def connect():
  client = await AsyncClient.create()

  bm = BinanceSocketManager(client)

  try:
    status = await client.get_system_status()
    print(status)
    ##await asyncio.gather(multiplex_socket(bm))
    await asyncio.create_task(multiplex_socket(bm))
  finally:
    await client.close_connection()

@bp.cli.command()
def run():
  loop = asyncio.get_event_loop()
  loop.run_until_complete(connect())

@bp.cli.command()
def test():
  print('hello')
