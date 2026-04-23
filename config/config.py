import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Security configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    TOKEN_EXPIRATION_SECONDS = int(os.environ.get('TOKEN_EXPIRATION_SECONDS', 3600))  # 1 hour


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False

class StagingConfig(Config):
    DEBUG = False

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Config,
    'staging': StagingConfig,
}


