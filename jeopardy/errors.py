class APIError(Exception):
    pass


class GQLError(APIError):
    pass


class AuthError(APIError):
    pass


class TokenSerializationError(AuthError):
    pass


class InvalidTokenError(AuthError):
    pass
