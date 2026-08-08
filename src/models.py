from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    summary = Column(String(512))
    status = Column(String(100))
    assignee = Column(String(200))
    labels = Column(JSON)
    epic = Column(String(100))
    raw = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class ConfluencePage(Base):
    __tablename__ = 'confluence_pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(512))
    url = Column(String(1024))
    raw = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
