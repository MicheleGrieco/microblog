"""
Module name: errors.py
Author: Michele Grieco
Description:
    This module initializes the error handling blueprint for the Flask application.
    It sets up a Blueprint named 'errors' and imports the error handlers from the handlers module.
"""

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
