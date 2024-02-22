import json
import time

base_dir = '/app/'
# base_dir = '/Users/surya.m/Documents/CIAECO/test/loveall-api-fast/'

with open(base_dir + 'config.json') as config_file:
    config_data = json.load(config_file)

ENV = config_data.get("API_ENV")


class Config:
    VERSION_INFO = '1.0.0'
    log_base_dir = config_data.get("log_base_dir")
    log_file = config_data.get("log_file")
    JWT_SECRET = config_data.get("auth").get("JWT_SECRET")
    JWT_ALGORITHM = config_data.get("auth").get("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = config_data.get("auth").get("ACCESS_TOKEN_EXPIRE_MINUTES")
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