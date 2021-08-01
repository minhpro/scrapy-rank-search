from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime,
    SmallInteger, Boolean, UniqueConstraint
)
from datetime import datetime

Base = declarative_base()

class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    target_site = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False, default='')
    rank = Column(Integer, nullable=False, default=0)
    last_update = Column(DateTime, nullable=False, default=datetime.utcnow)
    error_code = Column(SmallInteger, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    priority = Column(Integer, nullable=False, default=0)
    __table_args__ = (
        UniqueConstraint(content, target_site),
        {},
    )

    def __repr__(self):
        return "<Keyword(content='%s', target_site='%s', url='%s', rank='%d')>" % (
                             self.content, self.target_site, self.url, self.rank)