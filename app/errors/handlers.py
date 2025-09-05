"""
Module name: handlers.py
Author: Michele Grieco
Description:
    This module defines custom error handlers for the Flask application.
    It includes handlers for 404 (Not Found) and 500 (Internal Server Error) errors.
    The handlers render appropriate HTML templates and manage database sessions as needed.
Usage:
    - not_found_error: Handles 404 errors by rendering a '404.html' template.
    - internal_error: Handles 500 errors by rolling back the database session and rendering a '500.html' template.
"""

from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors by rendering a custom 404 error page.
    :param error: The error object representing the 404 error.
    :return: A tuple containing the rendered template and the 404 status code.
    """
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server errors by rolling back the database session
    and rendering a custom 500 error page.
    :param error: The error object representing the 500 error.
    :return: A tuple containing the rendered template and the 500 status code.
    """
    db.session.rollback()
    return render_template('errors/500.html'), 500
