from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tgbot.config import Config
from tgbot.models.base import BaseModel


async def create_db_engine_and_session_pool(config: Config) -> tuple[AsyncEngine, sessionmaker]:
    engine = create_async_engine(
        config.db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=100,
        max_overflow=200,
        future=True,
        echo=True if config.misc.log_level == 10 else False
    )

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    sqlalchemy_session_pool = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    return engine, sqlalchemy_session_pool
