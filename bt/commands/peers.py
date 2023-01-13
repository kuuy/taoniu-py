import time
from datetime import datetime

from socket import inet_ntoa
from struct import unpack

import libtorrent as lt

from flask import Blueprint

from bt.repositories import peers as repository

bp = Blueprint('peers', __name__)


@bp.cli.command()
def discovery():
  session = lt.session({
    'listen_interfaces': '[240e:380:1b68:8300:d401:b838:b42:31d6]:6881',
    'upload_rate_limit': 200000,
    'download_rate_limit': 200000,
    'active_downloads': 30,
    'alert_queue_size': 4000,
    'dht_announce_interval': 60,
    'auto_manage_startup': 30,
    'auto_manage_interval': 15,
  })
  session.set_alert_mask(lt.alert.category_t.all_categories)
  session.listen_on(6801, 6861)

  session.add_dht_router("router.utorrent.com", 6881)
  session.add_dht_router("router.bt.com", 6881)
  session.add_dht_router("dht.transmissionbt.com", 6881)
  session.add_dht_router("router.bitcomet.com", 6881)
  session.add_dht_router("dht.aelitis.com", 6881)

  timestamp = datetime.now().timestamp()
  while True:
    alerts = session.pop_alerts()
    for alert in alerts:
      if alert.category() & lt.alert.category_t.error_notification:
        continue
      if type(alert) is not lt.dht_pkt_alert:
        continue
      decoded = lt.bdecode(alert.pkt_buf)
      if not decoded:
        continue
      if decoded.get(b'y') == b'r':
        if b'nodes' in decoded[b'r']:
          sources = decode_nodes(decoded[b'r'][b'nodes'])
          if len(sources) > 0:
            timestamp = datetime.now().timestamp()
            repository.flush(
              decoded.get(b't').hex(),
              sources,
            )
        elif b'ip' in decoded:
          pass
        else:
          print('alert', alert)
      elif decoded.get(b'q') == b'get_peers':
        repository.save(
          decoded.get(b't').hex(),
          decoded[b'a'][b'info_hash'].hex(),
        )
      elif decoded.get(b'q') == b'find_node':
        pass
      elif decoded.get(b'q') == b'ping':
        pass
      else:
        print('alert', alert)

    if timestamp + 300 < datetime.now().timestamp():
      break

    time.sleep(1)

@bp.cli.command()
def metadata():
  repository.metadata()
  # infohash = ""
  # address = ""
  # stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # stream.settimeout(15)
  # stream.connect(address)
  #
  # send_handshake(stream, infohash)
  # packet = stream.recv(4096)

  # socket = socket(socket.AF_INET, socket.SOCK_STREAM)

def decode_nodes(nodes):
  n = []
  length = len(nodes)
  if (length % 26) != 0:
    return n

  ips = []
  for i in range(0, length, 26):
    id = nodes[i:i + 20].hex()
    ip = inet_ntoa(nodes[i + 20:i + 24])
    port = unpack("!H", nodes[i + 24:i + 26])[0]
    if ip not in ips:
      n.append((id, ip, port))
      ips.append(ip)

  return n
