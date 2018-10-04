import os


class Config:
    DEBUG = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')

    POSTGRES = {
        'user': os.getenv('DB_USER', 'notifications-app'),
        'pass': os.getenv('DB_PASS', 'P@55w0rd'),
        'db': os.getenv('DB_NAME', 'notifications-app'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
    }

    SQLALCHEMY_DATABASE_URI = \
        'postgresql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s' % POSTGRES

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    staging=StagingConfig,
    production=ProductionConfig
)
