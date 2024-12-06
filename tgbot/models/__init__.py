from sqlalchemy import Column, Integer, ForeignKey, Text
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
    curr_workspace_id = Column(
        Text, ForeignKey("workspaces.workspace_id", ondelete="SET NULL"), nullable=True
    )
    curr_database_id = Column(
        Text, ForeignKey("databases.database_id", ondelete="SET NULL"), nullable=True
    )


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workspace_name = Column(Text, nullable=False)
    workspace_id = Column(Text, unique=True, nullable=False)
    telegram_user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )


class Database(Base):
    __tablename__ = "databases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    database_name = Column(Text, nullable=False)
    database_id = Column(Text, unique=True, nullable=False)
    workspace_id = Column(
        Text, ForeignKey("workspaces.workspace_id", ondelete="CASCADE"), nullable=False
    )


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)
    title = Column(Text)
    category = Column(Text)
    database_id = Column(
        Text, ForeignKey("databases.database_id", ondelete="CASCADE"), nullable=False
    )
