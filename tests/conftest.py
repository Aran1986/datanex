# Location: datanex/tests/conftest.py

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.base import Base

@pytest.fixture
async def test_db():
    """دیتابیس تست"""
    engine = create_async_engine(
        "postgresql+asyncpg://admin:admin123@localhost:5432/bigdata_test",
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    yield async_session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()