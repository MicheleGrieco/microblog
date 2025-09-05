"""
Module name: auth.py
Author: Michele Grieco
Description:
    This module initializes the authentication blueprint for the Flask application.
    It sets up the blueprint and imports the routes associated with authentication.
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes
