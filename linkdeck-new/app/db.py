"""Database engine and session management."""
from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


def create_engine() -> AsyncEngine:
    db_url = f"sqlite+aiosqlite:///{settings.DB_PATH}"
    engine = create_async_engine(
        db_url,
        echo=settings.DEBUG,
        future=True,
        connect_args={"check_same_thread": False},
    )
    return engine


engine = create_engine()
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    from app.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Lightweight forward-only migration: add offers.code to older databases.
        result = await conn.exec_driver_sql("PRAGMA table_info(offers)")
        columns = {row[1] for row in result.fetchall()}
        if "code" not in columns:
            await conn.exec_driver_sql("ALTER TABLE offers ADD COLUMN code VARCHAR(40)")