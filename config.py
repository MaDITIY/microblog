import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mega-secret-key'
    POSTS_PER_PAGE = 10
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/microblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['microblog.app.maintain.email@gmail.com']