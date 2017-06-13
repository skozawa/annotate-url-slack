import os


class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True


class StagingConfig(Config):
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    DEBUG = True


class LocalConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


def config_by_env():
    env = os.getenv('APP_ENV', 'development')
    class_name = env.title() + 'Config'
    if class_name in globals():
        return globals()[class_name]()
    else:
        return DevelopmentConfig()


config = config_by_env()
