from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.db.session import get_db_session
from app.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Generator[TestClient]:
    database_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)

    def override_db_session() -> Generator[Session]:
        with testing_session() as session:
            yield session

    application = create_app()
    application.dependency_overrides[get_db_session] = override_db_session

    with TestClient(application) as test_client:
        yield test_client

    application.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()
