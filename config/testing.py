from config import DevelopmentConfig


class TestingConfig(DevelopmentConfig):
    TESTING = True
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'