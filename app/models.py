from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
)


class User(db.Model, UserMixin):
    """User model representing app user entity."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        """User model string representation."""
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """Generate password hash for given password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches self password hash."""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Generate user avatar."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(user_id: str) -> User:
    """Get user from DB to load to user session."""
    return User.query.get(int(user_id))


class Post(db.Model):
    """Post model representing users posts."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.body}>'
