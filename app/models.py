from datetime import datetime
from time import time
from typing import Any, Optional
from hashlib import md5
import json

from flask import current_app
from flask import url_for
from flask_login import UserMixin
import jwt
import redis
import rq
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
from app.mixins import PaginatedAPI
from app.mixins import Searchable


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
)


class User(db.Model, UserMixin, PaginatedAPI):
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
        lazy='dynamic',
    )
    messages_sent = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        backref='author',
        lazy='dynamic',
    )
    messages_received = db.relationship(
        'Message',
        foreign_keys='Message.recipient_id',
        backref='recipient',
        lazy='dynamic',
    )
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy='dynamic',
    )
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self) -> str:
        """User model string representation."""
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """Generate password hash for given password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches self password hash."""
        return check_password_hash(self.password_hash, password)

    def follow(self, user: 'User') -> None:
        """Follow given user."""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user: 'User') -> None:
        """Unfollow given user."""
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user: 'User') -> None:
        """Check if self is following given user."""
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def followed_posts(self):
        """Get all posts of people who are followed with own posts."""
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def avatar(self, size: int) -> str:
        """Generate user avatar."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # TODO: Add typing to verification methods.
    def get_reset_password_token(self, expires_in=600):
        """Get JWT token for password reset."""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        """Verify reset password token."""
        try:
            user_id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
        except Exception:
            return
        return User.query.get(user_id)

    # TODO: could be a property instead?
    def new_messages_count(self) -> int:
        """Gather unread messages."""
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time
        ).count()

    def add_notification(self, name: str, data: Any) -> None:
        """Add new notification for a self User."""
        self.notifications.filter_by(name=name).delete()
        notif = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(notif)

    def launch_task(
            self, name: str, description: str, *args: list, **kwargs: dict
    ) -> 'Task':
        """Launch background task linked to self user."""
        rq_job = current_app.task_queue.enqueue(
            f'app.tasks.{name}',
            self.id,
            *args, **kwargs
        )
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self) -> list:
        """Get self tasks which are in progress."""
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name: str) -> 'Task':
        """Get self in progress task by name."""
        return Task.query.filter_by(name=name, user=self, complete=False).first()

    def to_dict(self, include_email: bool = False) -> dict:
        """Build dict representation of User model"""
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': f'{self.last_seen.isoformat()}Z',
            'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('api.v1.get_user', id=self.id),
                'followers': url_for('api.v1.get_followers', id=self.id),
                'followed': url_for('api.v1.get_followed', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data: dict, new_user: bool = False) -> None:
        """Method to create/update User instance from dict."""
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


@login.user_loader
def load_user(user_id: str) -> User:
    """Get user from DB to load to user session."""
    return User.query.get(int(user_id))


class Post(db.Model, Searchable):
    """Post model representing users posts."""
    __tablename__ = 'posts'

    _fulltext_attrs = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language = db.Column(db.String(10))

    def __repr__(self) -> str:
        """Return Post representation."""
        return f'<Post {self.body}>'


class Message(db.Model):
    """DB model representing user private messages."""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Message object str representation."""
        return f'<Message {self.body}>'


class Notification(db.Model):
    """Class for representation of user notification."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self) -> dict:
        """Get notification payload."""
        return json.loads(str(self.payload_json))


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self) -> Optional[rq.job.Job]:
        """Get Redis Queue job by its ID."""
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self) -> int:
        """Get RQ job progress percentage."""
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
