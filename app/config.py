import json
import time

base_dir = '/Users/surya.m/Documents/CIAECO/loveall-api-fast/'

with open(base_dir + 'config.json') as config_file:
    config_data = json.load(config_file)

ENV = config_data.get("API_ENV")


class Config:
    VERSION_INFO = '1.0.0'
    log_base_dir = config_data.get("log_base_dir")
    log_file = config_data.get("log_file")
    start_time = time.time()


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config_data.get("DBS").get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'loveall': config_data.get('DBS').get('SQLALCHEMY_DATABASE_URI')
    }


class TestingConfig(Config):
    ENV = 'test'
    Debug = True
    SQLALCHEMY_DATABASE_URI = config_data.get("DBS").get('TEST_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'loveall': config_data.get('DBS').get('TEST_SQLALCHEMY_DATABASE_URI')
    }
    VERSION_INFO = '1.0.0'


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig
)