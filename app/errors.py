from flask import render_template

from app import app
from app import db


@app.errorhandler(404)
def not_found_error(error):
    """Custom Error handler for 404 code."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Custom Error handler for 500 code."""
    db.session.rollback()
    return render_template('500.html'), 500
