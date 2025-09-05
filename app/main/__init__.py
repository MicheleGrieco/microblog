"""
Module name: __init__.py
Author: Michele Grieco
Description:
    This module initializes the 'main' Blueprint for the Flask application.
    It sets up the Blueprint and imports the routes defined in the 'routes' module.
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
