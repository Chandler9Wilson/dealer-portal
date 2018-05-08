from secrets import db_username, db_password, flask_secret_key


class BaseConfig(object):

    # The secret key used in sessions cryptography
    SECRET_KEY = flask_secret_key

    # SQLALCHEMY Config
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + db_username + ':' + \
        db_password + '@localhost:5432/acmonitor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class SqlAlchemyDebug(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    TESTING = True
    # Sets login_required decorators to be ignored
    LOGIN_DISABLED = True
