import pytest
from fastapi.testclient import TestClient
from ..app import app


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)
