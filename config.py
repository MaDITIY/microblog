import os


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_uri = f'sqlite:///{os.path.join(basedir, "app.db")}'
postgres_db_name = 'microblog'
postgres_uri = f'postgresql:///{postgres_db_name}'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or postgres_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS', ['xavijo3307@ippals.com'])
