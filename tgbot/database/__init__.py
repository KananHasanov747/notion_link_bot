from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# SQLite database URI
db_url = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(db_url, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=True)
session = async_session()
