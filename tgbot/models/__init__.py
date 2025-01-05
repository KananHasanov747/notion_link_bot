from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


# SQLAlchemy Base
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    workspace_id = Column(Text, nullable=False)
    database_id = Column(Text, nullable=False)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)
    title = Column(Text)
    category = Column(Text)
    source = Column(Text)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    database_id = Column(
        Text, ForeignKey("users.database_id", ondelete="CASCADE"), nullable=False
    )
