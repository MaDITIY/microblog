from app import cli
from app import create_app
from app import db
from app.models import Message
from app.models import Notification
from app.models import Post
from app.models import Task
from app.models import User


# General App TODOs:
# TODO: Move pagination footer to a subtemplate.


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Message': Message,
        'Notification': Notification,
        'Task': Task,
    }
