"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    # "mysql+pymysql://root:19990704@mysql:3306/app"
    DBCLIENTNAME="mysql+pymysql://%s:%s@%s:%s/%s"%(environ.get("DB_USERNAME"),
                                                   environ.get("DB_PASSWORD"),
                                                   environ.get("DB_URL"),
                                                   environ.get("DB_PORT"),
                                                   environ.get("DB_NAME"))


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')