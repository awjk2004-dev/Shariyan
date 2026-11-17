import os
os.environ["DATABASE_URL"] = "sqlite:///./test_shريان.db"
os.environ["ADMIN_BOOTSTRAP_TOKEN"] = "test-bootstrap-token"
os.environ["SECRET_KEY"] = "test-only-secret-key-with-at-least-32-characters"

import pytest
from fastapi.testclient import TestClient

from backend.database import Base, engine
from backend.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)
