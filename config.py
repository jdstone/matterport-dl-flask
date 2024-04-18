import os
from datetime import timedelta
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


# class ProductionConfig(Config):
#     DEBUG = False


config = {
    'development': DevelopmentConfig,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}
