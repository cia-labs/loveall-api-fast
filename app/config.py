import json
import os
import time

base_dir = '/app/'
# base_dir = '/Users/surya.m/Documents/CIAECO/test/loveall-api-fast/'

ENV = os.getenv("API_ENV")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


class Config:
    VERSION_INFO = '1.0.0'
    JWT_SECRET = JWT_SECRET
    JWT_ALGORITHM = JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
    start_time = time.time()


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'loveall': os.getenv("SQLALCHEMY_DATABASE_URI")
}


class TestingConfig(Config):
    ENV = 'test'
    Debug = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'loveall': os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    }
    VERSION_INFO = '1.0.0'


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig
)