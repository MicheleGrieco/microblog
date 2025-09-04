"""
Module name: __init__.py
Author: Michele Grieco
Description:
    Application factory for the Flask microblog application.
    Initializes extensions and registers blueprints.
Usage:
    - create_app(config_class=Config): Create and configure the Flask app instance.
"""

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from elasticsearch import Elasticsearch


def get_locale() -> str | None:
    """
    Selects the best match for supported languages based on the client's
    Accept-Language header.
    :return: The best matching language code.
    """
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login' # type: ignore
login.login_message = _l('Please log in to access this page.') # type: ignore
mail = Mail()
moment = Moment()
babel = Babel()


def create_app(config_class=Config) -> Flask:
    """
    Application factory function to create and configure the Flask app.
    :param config_class: The configuration class to use.
    :return: Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions 
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    # Elasticsearch presents the challenge that it isn't wrapped by a Flask extension.
    # You cannot create the Elasticsearch instance in the global scope like we did above,
    # because to inizialize it we need access to app.config, which only becomes
    # available after the create_app() function is invoked. The solution here is to add
    # a elasticsearch attribute to the app instance in the application factory function.
    # Adding a new attribute to the app instance may seem a little strange,
    # but Python objects are not strict in their structure,
    # and new attributes can be added to them at any time.
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None # pyright: ignore[reportAttributeAccessIssue]

    # Blueprint registrations
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    # Logging configuration
    if not app.debug and not app.testing: # This ensures logging is not set up during testing or debugging
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from app import models
