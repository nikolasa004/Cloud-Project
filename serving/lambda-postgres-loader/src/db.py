from __future__ import annotations

import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """
    Creates and returns a SQLAlchemy engine for PostgreSQL.
    """

    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    database = os.environ["DB_NAME"]
    username = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]

    connection_string = (
        f"postgresql+psycopg2://"
        f"{username}:{password}@{host}:{port}/{database}"
    )

    return create_engine(
        connection_string,
        pool_pre_ping=True,
    )


def test_connection(engine: Engine) -> bool:
    """
    Verifies that PostgreSQL is reachable.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True

    except Exception:
        return False