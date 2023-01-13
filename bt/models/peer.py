from sqlalchemy import (
  String,
  Integer,
  JSON,
  Column,
  DateTime,
  func,
)

from bt import db

class Peer(db.Model):
  id = Column(String(20), primary_key=True)
  tid = Column(String(4), nullable=False)
  infohash = Column(String(40), nullable=False, unique=True)
  sources = Column(JSON, default=[], nullable=False)
  data = Column(JSON, default=[], nullable=False)
  status = Column(Integer, default=0, nullable=False)
  timeout_count = Column(Integer, default=0, nullable=False)
  streak_timeout_count = Column(Integer, default=0, nullable=False)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

  __tablename__ = 'bt_peers'
