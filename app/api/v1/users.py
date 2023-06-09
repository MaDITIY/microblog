from flask import jsonify
from flask import request

from app.api.v1 import bp
from app.models import User


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Get single user by ID."""
    user_dict = User.query.get_or_404(id).to_dict()
    return jsonify(user_dict)


@bp.route('/users', methods=['GET'])
def get_users():
    """Get all application users."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(
        query=User.query,
        page=page,
        per_page=per_page,
        endpoint='api.get_users',
    )
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass


@bp.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass


@bp.route('/users', methods=['POST'])
def create_user():
    pass


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
