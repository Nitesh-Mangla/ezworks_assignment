# app configuration file globally
import logging
from core import app
import os


class config:
    ENV = "production"
    DEBUG = False
    TESTING = False


# for development
class Development(config):
    ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = "VVHV213JHV21JV3H2V43V4V3"
    UPLOAD_FOLDER = os.path.abspath(os.getcwd())+"/medias"

    DB_HOST = 'localhost'
    DB_NAME = "faqservice"
    DB_USERNAME = "root"
    DB_PASSWORD = "root"
    DB_PORT = 3306

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'niteshmangla8860@gmail.com'
    MAIL_PASSWORD = 'sunilmangla'

    logging.basicConfig(filename='logs/event.log',
                        format='%(levelname)s %(asctime)s :: %(message)s',
                        level=logging.DEBUG)
