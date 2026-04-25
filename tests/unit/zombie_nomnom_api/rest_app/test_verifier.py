from unittest.mock import Mock, patch

import pytest
from zombie_nomnom_api.rest_app.authentication import get_verifier, VerifyToken
from jwt.exceptions import PyJWKClientError, DecodeError


@pytest.fixture(autouse=True)
def patch_jwks_client():
    with patch("zombie_nomnom_api.rest_app.authentication.jwt") as mock:
        yield mock.PyJWKClient.return_value


@pytest.fixture
def patch_jwt_decode(autouse=True):
    with patch("zombie_nomnom_api.rest_app.authentication.jwt") as mock:
        yield mock.decode


@pytest.fixture(autouse=True)
def cleanup_cache():
    yield
    get_verifier.cache_clear()


def test_get_verifier__when_called__returns_verify_token_object():

    assert isinstance(get_verifier(), VerifyToken)


def test_get_verifier__when_called_returns_a_cached_verifier_object():

    verifier = get_verifier()
    verifier2 = get_verifier()
    assert verifier is verifier2


def test_check_claims__when_called__returns_expected_result():

    verifier = get_verifier()
    result = verifier._check_claims({"scope": "a b"}, "scope", str, ["a", "b"])
    assert result == {"status": "success", "status_code": 200}


def test_verify__when_called__returns_expected_result(patch_jwt_decode):
    verifier = get_verifier()
    result = verifier.verify("token", None, None)
    assert isinstance(result, Mock)


def test_verify__when_decode_error_raised__returns_exception_with_expected_message(
    patch_jwks_client,
):
    verifier = get_verifier()
    patch_jwks_client.get_signing_key_from_jwt.side_effect = DecodeError("error")
    result = verifier.verify("token", None, None)
    assert result == {"status": "error", "message": "error"}


def test_verify__when_jwk_client_error_raised__returns_exception_with_expected_message(
    patch_jwks_client,
):
    verifier = get_verifier()

    patch_jwks_client.get_signing_key_from_jwt.side_effect = PyJWKClientError("error")
    result = verifier.verify("token", None, None)
    assert result == {"status": "error", "message": "error"}


def test_verify__when_list_of_scopes_are_in_parameter__returns_success_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"scope": "a b"}

    result = verifier.verify("token", scopes=["a", "b"])
    assert result == {"scope": "a b"}


def test_verify__when_string_of_scopes_are_in_parameter__returns_success_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"scope": "a b"}

    result = verifier.verify("token", scopes="a b")
    assert result == {"scope": "a b"}


def test_verify__when_scopes_are_not_in_payload__returns_error_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"permissions": ["a", "b"]}

    result = verifier.verify("token", scopes=["a", "b"])
    assert result == {
        "status": "error",
        f"message": "User does not have the required 'scope' claim.",
    }


def test_verify__when_scopes_are_wrong_in_scopes_list_in_payload__returns_error_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"scope": ["a", "b"]}

    result = verifier.verify("token", scopes=["c", "d"])
    assert result == {
        "status": "error",
        f"message": "User does not have the required 'scope' claim.",
    }


def test_verify__when_permissions_are_in_payload__returns_success_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"permissions": ["a", "b"]}

    result = verifier.verify("token", permissions=["a", "b"])
    assert result == {"permissions": ["a", "b"]}


def test_verify__when_permissions_are_not_in_payload__returns_error_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"scope": ["a", "b"]}

    result = verifier.verify("token", permissions=["c", "d"])
    assert result == {
        "status": "error",
        f"message": "User does not have the required 'permissions' claim.",
    }


def test_verify__when_permissions_are_wrong_in_permissions_list_in_payload__returns_error_result(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.return_value = {"permissions": ["a", "b"]}

    result = verifier.verify("token", permissions=["c", "d"])
    assert result == {
        "status": "error",
        f"message": "User does not have the required 'permissions' claim.",
    }


def test_verify__when_decode_exception_raised__returns_exception_with_expected_message(
    patch_jwt_decode,
):
    verifier = get_verifier()
    patch_jwt_decode.side_effect = Exception("error")
    result = verifier.verify("token", None, None)
    assert result == {"status": "error", "message": "error"}
