import os


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_uri = f'sqlite:///{os.path.join(basedir, "app.db")}'
postgres_db_name = 'microblog'
postgres_uri = f'postgresql:///{postgres_db_name}'

rdms_name_uri_map = {
    'postgresql': postgres_uri,
    'sqlite': sqlite_uri,
}

RDMS_NAME = os.environ.get('RDMS_NAME', 'sqlite')
DEV_DB_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or rdms_name_uri_map[RDMS_NAME]
TEST_DB_URI = 'sqlite://'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    TESTING = int(os.environ.get('TESTING', '0'))
    SQLALCHEMY_DATABASE_URI = TEST_DB_URI if TESTING else DEV_DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE', 5))

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', '0'))
    MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL', '1'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS', ['microblog235@gmail.com'])

    LANGUAGES = os.environ.get('LANGUAGES', '').split(',') or ['en', 'ru', 'by']
    APP_TRANSLATOR = os.environ.get('APP_TRANSLATOR')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    MS_TRANSLATOR_LOCATION = os.environ.get('MS_TRANSLATOR_LOCATION')

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
