from contextlib import contextmanager
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = "sqlite:///data.db"


# echo=False to avoid verbose SQL logs in console
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

