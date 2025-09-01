from contextlib import contextmanager
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine
import sqlite3


DATABASE_URL = "sqlite:///data.db"


# echo=False to avoid verbose SQL logs in console
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
    _migrate_add_casa_link()


def _migrate_add_casa_link() -> None:
    # best-effort migration: add column if missing
    try:
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(casa)")
            cols = [row[1] for row in cur.fetchall()]
            if "link" not in cols:
                cur.execute("ALTER TABLE casa ADD COLUMN link TEXT")
                conn.commit()
    except Exception:
        # ignore if fails; table may not exist yet
        pass


@contextmanager
def get_session() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

