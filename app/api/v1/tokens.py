from flask import g
from flask import jsonify

from app import db
from app.api.v1 import bp
from app.api.v1.auth import basic_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """Get auth token."""
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


def revoke_token():
    pass
