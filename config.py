import os

# Taken from: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(16))
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    API_KEY = os.getenv('API_KEY')

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # in memory db
    #SQLALCHEMY_ECHO = True
