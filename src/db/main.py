from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.settings import Settings


def make_connection(settings: Settings) -> AsyncEngine:
    conn = create_async_engine(settings.db_url, echo=settings.debug, future=True)

    return conn


def get_sessionmaker(conn: AsyncEngine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=conn, expire_on_commit=False, class_=AsyncSession)


def destroy_connection(conn: AsyncEngine):
    conn.sync_engine.dispose(close=True)
