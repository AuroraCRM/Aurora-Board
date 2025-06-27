import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession # Renamed to avoid conflict
from fastapi.testclient import TestClient
import os

from aurora_board.main import app, get_db
from aurora_board.database import Base
from aurora_board import models # Ensure models are imported to be created by Base.metadata.create_all

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # Needed only for SQLite
    poolclass=StaticPool, # Use StaticPool for SQLite in-memory for tests
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the in-memory database
Base.metadata.create_all(bind=engine)

# Dependency override for tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: SQLAlchemySession):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_board(db_session: SQLAlchemySession):
    from aurora_board import services, schemas
    board_create = schemas.BoardCreate(name="Test Board", description="A board for testing")

    db_board = models.Board(name=board_create.name, description=board_create.description)
    db_session.add(db_board)
    db_session.commit()
    db_session.refresh(db_board)
    return db_board

@pytest.fixture(scope="function")
def test_list(db_session: SQLAlchemySession, test_board: models.Board):
    from aurora_board import services, schemas
    db_list = models.List(name="Test List 1", board_id=test_board.id, position=1)
    db_session.add(db_list)
    db_session.commit()
    db_session.refresh(db_list)
    return db_list

# Example pytest.ini in `aurora-board/backend/`:
# [pytest]
# python_files = test_*.py tests_*.py *_test.py *_tests.py
# pythonpath = src
