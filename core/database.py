from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from .config import settings
from models import Org, OutboundItem, Template, User

postgres_url = settings.DB_URL
connect_args = {}
# engine = create_engine(postgres_url,connect_args=connect_args)


engine = create_async_engine(postgres_url, echo=False, future=True, connect_args=connect_args)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def org_scope_query(session, model, org_id):
    return session.execute(select(model).where(model.org_id == org_id))
