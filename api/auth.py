"""_summary_

Returns:
    _type_: _description_
"""

from functools import wraps

import jwt
from flask import current_app, g, request

from api.errors import AuthError


def get_token_auth_header() -> str:
    """_summary_

    Raises:
        AuthError: _description_
        AuthError: _description_
        AuthError: _description_
        AuthError: _description_

    Returns:
        str: _description_
    """

    # Check if token is present in request headers
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            }
        )
    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            }
        )
    if len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found"})
    if len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            }
        )
    token = parts[1]
    return token


def requires_auth(func):
    """_summary_

    Args:
        func (_type_): _description_
    """

    @wraps(func)
    def wrapper(*args, **kwargs):  # pylint: disable=unused-argument
        token = get_token_auth_header()
        try:
            payload = jwt.decode(
                jwt=token,
                key=current_app.config["SECRET_KEY"],
                algorithms=["HS256", "HS512"],
            )
        except jwt.ExpiredSignatureError as expired_sign_error:
            raise AuthError(
                {"code": "token_expired", "description": "token is expired"}
            ) from expired_sign_error
        except Exception as exc:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication" " token.",
                }
            ) from exc
        g.authenticated_user = payload
        return func(*args, **kwargs)

    return wrapper
