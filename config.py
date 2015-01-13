import os
from distutils.util import strtobool

class Config(object):
    DEBUG = True
    REDIS_URL = os.environ.get('REDISTOGO_URL')

    AUTH_USER = 'admin'

class ConfigProduction(Config):
    DEBUG = strtobool(os.environ.get('DEBUG', 'false'))
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    AUTH_PASS = os.environ.get('AUTH_PASS')

class ConfigLocal(Config):
    APPLICATION_ROOT = ''
    REDIS_URL = 'redis://localhost:6379/0'
    AUTH_PASS = 'seekrit'