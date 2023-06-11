from flask import g
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth
from flask.typing import ResponseReturnValue

from app.models import User
from app.api.v1.errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username: str, password: str) -> True:
    """Verify user password."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@token_auth.verify_token
def verify_token(token: str) -> bool:
    """Verify given user auth token."""
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@basic_auth.error_handler
@token_auth.error_handler
def auth_error_handler() -> ResponseReturnValue:
    """Handle auth error."""
    return error_response(401)
