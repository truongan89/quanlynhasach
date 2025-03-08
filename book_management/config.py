#book_management/config
from os import environ
from dotenv import load_dotenv
from app.constants import *

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{environ.get('MYSYSQL_USERNAME')}:{environ.get('MYSQL_PASSWORD')}@{environ.get('MYSQL_HOST')}/bookstore"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = JWT_DUE_DATE  # Thời gian hết hạn token

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Chọn môi trường
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}