import pytest
from fastapi.testclient import TestClient
from myapp.web.app import app


@pytest.fixture(scope='session')
def client():
    # Needs to run in context-manager so that
    # setup_app is run on start-up
    with TestClient(app) as client:
        yield client
