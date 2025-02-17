import pytest
from fastapi.testclient import TestClient
from myapp.web.app import app


@pytest.fixture()
def client():
    t = TestClient(app)
    yield t
