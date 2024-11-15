import os

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = os.getenv("SQLITE_PATH", "database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def save(session: Session, model: SQLModel):
    session.add(model)
    session.commit()
    session.refresh(model)

SessionDep = Annotated[Session, Depends(get_session)]
