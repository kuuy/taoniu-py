import hashlib
import random
import socket
from datetime import (
  datetime,
  timedelta,
)

from sqlalchemy import desc
from xid import Xid

from bt import db
from bt.models.peer import Peer

BT_PROTOCOL = 'BitTorrent protocol'

def save(tid, infohash):
  entity = db.session.query(Peer).filter_by(
    infohash=infohash,
  ).first()
  if entity is None:
    entity = Peer(
      id=Xid().string(),
      tid=tid,
      infohash=infohash,
    )
  else:
    entity.tid = tid
  db.session.add(entity)
  db.session.commit()

def flush(tid, sources):
  entity = db.session.query(Peer).filter_by(
    tid=tid,
  ).order_by(desc(Peer.updated_at)).first()
  if entity is None:
    return
  if datetime.now() - entity.updated_at.replace(tzinfo=None) > timedelta(seconds=15):
    return
  entity.status = 1
  entity.sources = sources
  db.session.add(entity)
  db.session.commit()

def metadata():
  entity = db.session.query(Peer).filter_by(
    status=1,
  ).order_by(desc(Peer.updated_at)).first()
  if entity is None:
    return
  for source in entity.sources:
    print(f'magnet:?xt=urn:btih:{entity.infohash}')
    try:
      stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      stream.settimeout(15)
      stream.connect(tuple(source[1:]))
      handshake(stream, entity.infohash)
      packet = stream.recv(4096)
      print('packet:', len(packet))
      stream.close()
    except socket.timeout:
      print('message timeout')
      pass
    except Exception as e:
      print(e.with_traceback())
    finally:
      stream.close()
    break

def nodeId():
  id = ''.join(chr(random.randint(0, 255)) for _ in range(20))
  return hashlib.sha1(id.encode('utf-8')).digest()

def preheader():
  bt_header = chr(len(BT_PROTOCOL)) + BT_PROTOCOL
  ext_bytes = "\x00\x00\x00\x00\x00\x10\x00\x00"
  return (bt_header + ext_bytes).encode('utf-8')

def handshake(stream, infohash):
  id = nodeId()
  packet = preheader() + bytes.fromhex(infohash) + id
  stream.send(packet)