"""
Module Name: __init__.py
Author: Michele Grieco
Created: 2025-06-12
Description:
    This module initializes the Flask application and its extensions.
    It sets up the application configuration, database, migration engine, and login manager.
    It also configures logging for the application, including email notifications for errors.

Usage:
    This module is imported by the main application and is used to set up the Flask app.
    It initializes the database, migration engine, and login manager, and configures logging.
"""

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # Flask wrapper for Alembic, a database migration framework for SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # Database instance
migrate = Migrate(app, db) # Database migration engine
login = LoginManager(app)
mail = Mail(app)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

# Endpoint for login view
login.login_view = 'login' # type: ignore
login.login_message = _l('Please log in to access this page.') #type: ignore

# Email logger enabled only when app is running without debug mode
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        
        # File logging
        # Categories: DEBUG, INFO, WARNING, ERROR, CRITICAL
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        # Custom formatting
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

from app import routes, models, errors