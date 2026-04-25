from functools import cache
from fastapi.security import HTTPBearer
import jwt
from jwt.exceptions import PyJWKClientError, DecodeError
from zombie_nomnom_api import configs


token_auth_scheme = HTTPBearer()


def create_error_json(message: str) -> dict[str, str]:
    return {"status": "error", "message": message}


class VerifyToken:
    def __init__(self, configs=configs):
        """
        Args:
            configs (zombie_nomnom_api.Configs): The Configs that hold the domain for the oauth server.

        Attributes:
            config (zombie_nomnom_api.Configs): The Configs that hold the domain for the oauth server.
            jwks_client (jwt.PyJWKClient): A jwt client that is used to verify the tokens.
        """
        self.config = configs

        jwks_url = f"https://{self.config.oauth_domain}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self, token: str, permissions: list = None, scopes: list | str = None):
        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        except PyJWKClientError as error:
            return create_error_json(str(error))
        except DecodeError as error:
            return create_error_json(str(error))

        try:
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self.config.oauth_algorithms,
                audience=self.config.oauth_audience,
                issuer=self.config.oauth_issuer,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        if scopes:
            result = self._check_claims(
                payload,
                "scope",
                str,
                scopes if isinstance(scopes, list) else scopes.split(" "),
            )
            if result.get("status") == "error":
                return result

        if permissions:
            result = self._check_claims(payload, "permissions", list, permissions)
            if result.get("status") == "error":
                return result

        return payload

    def _check_claims(
        self, payload: dict, claim_name: str, claim_type: type, expected_value: list
    ):

        payload_claim = payload.get(claim_name)
        if payload_claim is None or not isinstance(payload[claim_name], claim_type):
            return create_error_json(
                f"User does not have the required '{claim_name}' claim."
            )
        result = {"status": "success", "status_code": 200}

        if claim_name == "scope":
            payload_claim = payload_claim.split(" ")

        for value in expected_value:
            if value not in payload_claim:
                return create_error_json(
                    f"User does not have the required '{claim_name}' claim."
                )
        return result


@cache
def get_verifier() -> VerifyToken:
    return VerifyToken()
