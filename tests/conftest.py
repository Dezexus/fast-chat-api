import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import pool, text

from app.main import app
from app.core.db import get_db
from app.core.config import settings
from app.models.base import Base


@pytest.fixture(scope="session")
async def db_engine():
    """Создает движок БД и таблицы на время всей сессии тестов."""
    engine = create_async_engine(
        settings.DATABASE_URL, poolclass=pool.NullPool, echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет чистую сессию для каждого теста."""
    async_session_factory = async_sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with async_session_factory() as session:
        yield session
        # Быстрая очистка данных после теста
        await session.execute(
            text("TRUNCATE TABLE messages, chats RESTART IDENTITY CASCADE")
        )
        await session.commit()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Асинхронный HTTP-клиент с переопределенной зависимостью БД."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
