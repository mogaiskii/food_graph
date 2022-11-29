from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from settings import Settings


def make_connection(settings: Settings) -> AsyncEngine:
    return create_async_engine(settings.get_db_url(), echo=settings.debug, future=True)


def get_sessionmaker(conn: AsyncEngine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=conn, expire_on_commit=False, class_=AsyncSession)


def destroy_connection(conn: AsyncEngine):
    conn.sync_engine.dispose(close=True)
