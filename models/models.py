import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel


class Org(SQLModel, table=True):
    __tablename__ = "Org"
    __table_args__ = {"schema": "marketplace"}


    id: uuid.UUID = Field(default=None, sa_column=Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()))
    name: str = Field(index=True)
    prefix: str = Field(
        sa_column=Column("prefix", Text, nullable=False, unique=True)
    )

    secret_name: str

    active: bool = Field(default=True, nullable=False)


    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    users: list["User"] = Relationship(back_populates="org")



class User(SQLModel, table = True):
    __tablename__ = "User"
    __table_args__ = {"schema": "marketplace"}


    id: uuid.UUID = Field(default=None, sa_column=Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()))
    password: str
    org_id: uuid.UUID = Field(foreign_key="marketplace.Org.id")
    role: str = "member"
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    org: Optional["Org"] = Relationship(back_populates=None)



class Template(SQLModel, table=True):
    __tablename__ = "template"
    __table_args__ = {"schema": "marketplace"}


    id: uuid.UUID = Field(default=None, sa_column=Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()))
    org_id: uuid.UUID = Field(foreign_key="marketplace.Org.id")
    name: str = Field(nullable=False)                    # e.g., "CSV v1" or "Flipkart v2"
    marketplace: Optional[str] = None                    # set only when role == 'output'
    schema: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True),
    )

    version: int = Field(default=1, nullable=False)
    active: bool = Field(default=True, nullable=False)


    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)



class OutboundItem(SQLModel, table=True):
    __tablename__ = "items"
    __table_args__ = {"schema": "marketplace"}


    id: uuid.UUID = Field(default=None, sa_column=Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()))
    org_id: uuid.UUID = Field(foreign_key="marketplace.Org.id")
    template_id: uuid.UUID = Field(foreign_key="marketplace.template.id")
    data: Dict[str, Any] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True),
    )
   # canonical, marketplace-shaped payload
    status: str = Field(default="queued", nullable=False)  

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


if __name__ == "__main__":

    import asyncio
    import os
    from sqlmodel import SQLModel
    from sqlalchemy.ext.asyncio import create_async_engine
    from dotenv import load_dotenv
    from sqlalchemy.sql import text


    DB_URL = os.environ["DB_URL"]
    engine = create_async_engine(DB_URL, echo=True, future=True)

    async def init_models():
        async with engine.begin() as conn:
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS marketplace;"))

            await conn.run_sync(SQLModel.metadata.create_all)

    asyncio.run(init_models())
