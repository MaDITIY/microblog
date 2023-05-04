from flask import render_template

from app import app
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    """Custom Error handler for 404 code."""
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """Custom Error handler for 500 code."""
    db.session.rollback()
    return render_template('errors/500.html'), 500