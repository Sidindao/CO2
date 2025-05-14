from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import config
import models

DATABASE_URL = config.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(models.Base.metadata.create_all)
        except Exception:
            pass

async def close_db():
    await engine.dispose()

async def get_db():
    async with SessionLocal() as session:
        yield session