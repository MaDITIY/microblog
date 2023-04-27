import os


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_uri = f'sqlite:///{os.path.join(basedir, "app.db")}'
postgres_db_name = 'microblog'
DEV_DB_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or f'postgresql:///{postgres_db_name}'
TEST_DB_URI = 'sqlite://'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    TESTING = int(os.environ.get('TESTING_MODE', '0'))
    SQLALCHEMY_DATABASE_URI = TEST_DB_URI if TESTING else DEV_DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_POSTS_PER_PAGE = 10

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', '0'))
    MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL', '1'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS', ['microblog235@gmail.com'])
