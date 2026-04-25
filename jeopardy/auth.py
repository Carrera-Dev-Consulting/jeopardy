from logging import getLogger

from fastapi import Depends, Request
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic_settings import BaseSettings, SettingsConfigDict
import jwt

from jeopardy.errors import InvalidTokenError, TokenSerializationError
from jeopardy.models import User

logger = getLogger(__name__)


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
    )

    jwt_secret: str = "some-super-secret-secret-that-is-secret-probably"
    jwt_algorithm: str = "HS256"
    jwt_audience: str = "cdc-jeopardy"
    jwt_issuer: str = "cdc-jeopardy"


auth_settings = AuthSettings()


def parse_token(token: str) -> User:
    try:
        raw_payload = jwt.decode(
            token,
            auth_settings.jwt_secret,
            algorithms=[auth_settings.jwt_algorithm],
            audience=[auth_settings.jwt_audience],
            issuer=[auth_settings.jwt_issuer],
        )
        # TODO: Consider refreshing permissions
        return User.model_validate(raw_payload)
    except Exception as e:
        logger.error(f"Failed to parse token: {e}", exc_info=True)
        raise InvalidTokenError(e)


def serialize_token(user: User) -> str:
    try:
        return jwt.encode(
            user.model_dump(mode="json"),
            auth_settings.jwt_secret,
            algorithm=auth_settings.jwt_algorithm,
            audience=auth_settings.jwt_audience,
            issuer=auth_settings.jwt_issuer,
        )
    except Exception as e:
        logger.error(f"Failed to serialize token: {e}", exc_info=True)
        raise TokenSerializationError(e)


BEARER_SCHEMA = HTTPBearer()


# Use Fastapi Built in Schema Parser
def get_request_credential(
    scheme: HTTPAuthorizationCredentials = Depends(BEARER_SCHEMA),
):
    return scheme.credentials


# Just forward the token to the parser
def parse_user(token: str = Depends(get_request_credential)) -> User | None:
    return parse_token(token)
