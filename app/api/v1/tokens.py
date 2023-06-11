from flask import g
from flask import jsonify
from flask.typing import ResponseReturnValue

from app import db
from app.api.v1 import bp
from app.api.v1.auth import basic_auth
from app.api.v1.auth import token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token() -> ResponseReturnValue:
    """Get auth token."""
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token() -> tuple:
    """Revoke current user token."""
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
