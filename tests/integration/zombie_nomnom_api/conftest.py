from fastapi.testclient import TestClient
import pytest
from zombie_nomnom_api.server import fastapi_app


@pytest.fixture
def api_client():
    return TestClient(app=fastapi_app)
