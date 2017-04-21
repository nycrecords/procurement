import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/procurement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = 'localhost'
    MAIL_SERVER = 'doittsmtp.nycnet'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Procurement]'
    FLASKY_MAIL_SENDER = 'Procurement Admin <donotreply@records.nyc.gov>'
    FLASKY_ADMIN = os.environ.get('PROCUREMENT_ADMIN')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024
    COST_LIMIT = 1000

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/procurement'
    SQLALCHEMY_DATABASE_URI = 'postgresql://developer@127.0.0.1:5432/procurement'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/procurement'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/procurement'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
