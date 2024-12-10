from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from tgbot.data.config import DATABASE_URL

# SQLite database URI
db_url = DATABASE_URL
engine = create_async_engine(db_url, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=True)
session = async_session()
