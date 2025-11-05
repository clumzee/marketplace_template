from ..models import User, Org, Template, OutboundItem
from sqlmodel import create_engine, SQLModel,Session

postgres_url = f"postgresql://postgres:root@localhost:5432/postgres"
connect_args = {"options":"-c search_path=dev_ai_ml"}
engine = create_engine(postgres_url,connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
