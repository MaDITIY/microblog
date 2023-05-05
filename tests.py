from datetime import datetime
from datetime import timedelta

from unittest import main
from unittest import TestCase

from app import db
from app import create_app
from app.models import Post
from app.models import User
from config import Config


class TestConfig(Config):
    """Config class for testing purpouses"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestUser(TestCase):
    """Test class to test User model."""
    def setUp(self) -> None:
        """Class setup."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        """Class teardown."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Test password hash generated is secure enough."""
        user = User(username='susan')
        user.set_password('cat')
        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('cat'))

    def test_avatar(self):
        """Test User model generates correct avatar link."""
        user = User(username='john', email='john@example.com')
        self.assertEqual(
            user.avatar(128),
            'https://www.gravatar.com/avatar/'
            'd4c74594d841139328695756648b6bd6?d=identicon&s=128'
        )

    def test_follow(self):
        """Test basic cases of follow functionality."""
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user1.followers.all(), [])

        user1.follow(user2)
        db.session.commit()

        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, 'susan')

        self.assertFalse(user2.is_following(user1))
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, 'john')

        user1.unfollow(user2)
        db.session.commit()

        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    def test_followed_posts(self):
        """Test cases for the followed_posts functionality."""
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        user3 = User(username='mary', email='mary@example.com')
        user4 = User(username='david', email='david@example.com')
        db.session.add_all([user1, user2, user3, user4])

        now = datetime.utcnow()
        post1 = Post(
            body='john post', author=user1, timestamp=now + timedelta(seconds=1))
        post2 = Post(
            body='susan post', author=user2, timestamp=now + timedelta(seconds=4))
        post3 = Post(
            body='mary post', author=user3, timestamp=now + timedelta(seconds=3))
        post4 = Post(
            body='david post', author=user4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        user1.follow(user2)
        user1.follow(user4)
        user2.follow(user3)
        user3.follow(user4)
        db.session.commit()

        user1_posts = user1.followed_posts().all()
        user2_posts = user2.followed_posts().all()
        user3_posts = user3.followed_posts().all()
        user4_posts = user4.followed_posts().all()
        self.assertEqual(user1_posts, [post2, post4, post1])
        self.assertEqual(user2_posts, [post2, post3])
        self.assertEqual(user3_posts, [post3, post4])
        self.assertEqual(user4_posts, [post4])


if __name__ == '__main__':
    main(verbosity=2)
