from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Untuk Neon: ganti ?ssl=true dengan ?sslmode=require di URL
# tapi pakai format yang asyncpg mengerti
DATABASE_URL = settings.DATABASE_URL.replace(
    "?ssl=true", ""
).replace(
    "postgresql+asyncpg://", "postgresql+asyncpg://"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "ssl": "require"
    }
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
