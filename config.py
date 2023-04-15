import os


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_uri = f'sqlite:///{os.path.join(basedir, "app.db")}'
postgres_db_name = 'microblog'
postgres_uri = f'postgresql:///{postgres_db_name}'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or postgres_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
