import os
import sys
from dotenv import dotenv_values
import redis

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    APP_NAME = os.environ.get('APP_NAME', 'api_server')
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')
    REDISPASS= os.environ.get('REDISPASS')
    REDISURL = os.environ.get('REDISURL', '192.168.1.7')
    REDISPORT = os.environ.get('REDISPORT', 6379)
    REDISDB = os.environ.get('REDISDB', 0)

    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def init_db(app):
        return redis.StrictRedis(
            host=REDISURL,
            password=REDISPASS,
            port=REDISPORT,
            db=REDISDB
        )

class DevelopmentConfig(Config):
    DEBUG = True
    # ASSETS_DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DEV_DATABASE_URL',
    #     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')

config = {
    'development': DevelopmentConfig
}
