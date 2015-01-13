import os
from distutils.util import strtobool

class Config(object):
    DEBUG = True
    REDIS_URL = os.environ.get('REDISTOGO_URL')

class ConfigProduction(Config):
    DEBUG = strtobool(os.environ.get('DEBUG', 'false'))
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT')
    SECRET_KEY = os.environ.get('SECRET_KEY')

class ConfigTesting(Config):
    TESTING = True
    APPLICATION_ROOT = ''
    REDIS_URL = 'redis://localhost:6379/0'