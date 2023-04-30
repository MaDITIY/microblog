from app import app
from app import cli
from app import db
from app.models import Post
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
