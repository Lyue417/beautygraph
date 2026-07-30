"""Shared database connection for BeautyGraph."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create a .env file based on .env.example."
    )

ENGINE: Engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)


def test_connection() -> dict[str, str]:
    """Return basic database information to verify connectivity."""
    with ENGINE.connect() as connection:
        row = connection.execute(
            text(
                """
                SELECT
                    current_database() AS database_name,
                    current_user AS user_name,
                    version() AS postgres_version
                """
            )
        ).mappings().one()

    return dict(row)


if __name__ == "__main__":
    info = test_connection()
    print(f"Database: {info['database_name']}")
    print(f"User: {info['user_name']}")
    print(f"Version: {info['postgres_version']}")
