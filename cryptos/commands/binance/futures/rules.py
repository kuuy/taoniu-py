import urllib3
import json

from flask import Blueprint

bp = Blueprint('rules', __name__)

@bp.cli.command()
def crawl():
  url = 'https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true'
  http = urllib3.PoolManager()
  resp = http.request('GET', url)
 
  if resp.status != 200:
    return

  data = json.loads(resp.data)
  if data['code'] != '000000':
    return

  for item in data['data']:
    if item['q'] != 'USDT':
      continue
    if item['st'] != 'TRADING':
      continue
    
    print('{} {} {}'.format(item['s'], item['ts'], item['qv']))
  


