import json
from unittest.mock import patch, Mock, AsyncMock
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pytest

from zombie_nomnom_api.server import _version, fastapi_app, hydrate_user


def test_server__when_module_loaded__sets_fastapi_version_to_version_in_file():
    assert fastapi_app.version == _version


@pytest.fixture
def patch_get_verifier():
    with patch("zombie_nomnom_api.server.get_verifier") as mock:
        yield mock


@pytest.fixture
def patch_token_auth_scheme():
    with patch(
        "zombie_nomnom_api.server.token_auth_scheme", new_callable=AsyncMock
    ) as mock:
        yield mock


@pytest.fixture
def mock_api_request():
    return Mock()


@pytest.fixture
def mock_call_next():
    return AsyncMock()


async def test_hydrate_user__when_token_exists_and_is_verified__adds_user_to_state(
    patch_get_verifier,
    patch_token_auth_scheme,
    mock_api_request,
    mock_call_next,
):

    verifier = patch_get_verifier.return_value
    user_data = {}
    verifier.verify.return_value = user_data

    await hydrate_user(mock_api_request, mock_call_next)

    assert mock_api_request.state.user == user_data


async def test_hydrate_user__when_token_exists_and_is_not_verified__does_not_add_user_to_state(
    patch_get_verifier,
    patch_token_auth_scheme,
    mock_api_request,
    mock_call_next,
):

    verifier = patch_get_verifier.return_value
    verifier.verify.return_value = {"status": "error", "status_code": 403}

    result = await hydrate_user(mock_api_request, mock_call_next)
    assert isinstance(result, JSONResponse)
    body = json.loads(result.body)
    assert result.status_code == 403
    assert body["status"] == "error"
    assert "user" not in body


async def test_hydrate_user__when_token_does_not_exist__does_not_add_user_to_state(
    patch_get_verifier,
    patch_token_auth_scheme,
    mock_api_request,
    mock_call_next,
):
    patch_token_auth_scheme.side_effect = HTTPException(status_code=401)

    result = await hydrate_user(mock_api_request, mock_call_next)
    assert isinstance(result, JSONResponse)
    body = json.loads(result.body)
    assert result.status_code == 401
    assert body["message"] == "Not Authenticated"
    assert body["status"] == "error"
    assert "user" not in body


async def test_hydrate_user_when_exception_throws_not_authenticated__does_not_add_user_to_state(
    patch_get_verifier,
    patch_token_auth_scheme,
    mock_api_request,
    mock_call_next,
):
    patch_token_auth_scheme.side_effect = HTTPException(
        status_code=401, detail="Not authenticated"
    )

    result = await hydrate_user(mock_api_request, mock_call_next)
    assert isinstance(result, AsyncMock)
