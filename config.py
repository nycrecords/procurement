import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery settings
    CELERY_RESULT_BACKEND = SQLALCHEMY_DATABASE_URI # Use the same database, no need for another
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_IMPORTS = [] # Add tasks here

    # Mail Settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = os.environ.get("MAIL_PORT") or 2525
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or None
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or None
    MAIL_SENDER = os.environ.get("MAIL_SENDER") or "donotreply@records.nyc.gov"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Procurement]'
    FLASKY_MAIL_SENDER = 'Procurement Admin <donotreply@records.nyc.gov>'

    FLASKY_ADMIN = os.environ.get('PROCUREMENT_ADMIN')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024
    COST_LIMIT = 1000

    # Authentication Settings
    USE_SAML = os.environ.get('USE_SAML') == "True"
    SAML_PATH = os.environ.get('SAML_PATH')

    # Session Settings
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_FILE_THRESHOLD = 100

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


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
