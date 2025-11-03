from typing import Annotated, List, Optional
import uuid

from datetime import datetime

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select



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




# sqlite_file_name = "database.db"
postgres_url = f"postgresql://postgres:root@localhost:5432/postgres"
connect_args = {"check_same_thread": False}
engine = create_engine(postgres_url,)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


create_db_and_tables()

# def get_session():
    # with Session(engine) as session:
        # yield session
# 
# SessionDep = Annotated[Session, Depends(get_session)]
# 