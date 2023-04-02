import os
#from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
#from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_PROD')

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SECRET_KEY ="cualquier_palabra"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI_DEV')


    """
    app.config['DEBUG']=True
    app.config['ENV']='development'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SECRET_KEY'] ="cualquier_palabra"
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    """
