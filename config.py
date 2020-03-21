import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mega-secret-key'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/microblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
