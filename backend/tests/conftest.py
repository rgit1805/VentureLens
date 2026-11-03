import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.core.config import settings


@pytest.fixture(scope="session")
def test_engine():
    test_url = make_url(settings.database_url).set(
        database="venturelens_test"
    )

    if test_url.database != "venturelens_test":
        raise RuntimeError("Unsafe integration test database.")

    engine = create_engine(test_url)

    try:
        with engine.connect() as connection:
            database_name = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if database_name != "venturelens_test":
                raise RuntimeError(
                    f"Connected to unexpected database: {database_name}"
                )

            vector_exists = connection.execute(
                text("""
                    SELECT EXISTS (
                        SELECT 1
                        FROM pg_extension
                        WHERE extname = 'vector'
                    )
                """)
            ).scalar_one()

            if not vector_exists:
                raise RuntimeError("pgvector extension is missing.")

        yield engine

    finally:
        engine.dispose()


@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session

    finally:
        session.close()

        # Undo all database changes made by this test,
        # including changes committed by application services.
        if transaction.is_active:
            transaction.rollback()

        connection.close()