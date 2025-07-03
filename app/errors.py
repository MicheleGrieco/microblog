"""
Module Name: errors.py
Author: Michele Grieco
Created: 2025-06-29
Description:
    This module handles error pages for the Flask application.
    It defines custom error handlers for 404 (Not Found) and 500 (Internal Server Error) errors.
    The error handlers render specific HTML templates for each error type.    

Usage:
    This module is imported by the main application and is used to handle errors globally.
    The error handlers are registered with Flask using the `@app.errorhandler` decorator.
"""

from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    """
    Custom error handler for 404 Not Found errors.
    Renders the 404 error page when a requested resource is not found.
    :param error: The error object containing details about the 404 error.
    :return: Rendered HTML template for the 404 error page.
    :rtype: tuple
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Custom error handler for 500 Internal Server Error.
    Renders the 500 error page when an internal server error occurs.
    Rolls back the database session to maintain integrity.
    :param error: The error object containing details about the 500 error.
    :return: Rendered HTML template for the 500 error page.
    :rtype: tuple
    """
    db.session.rollback()
    return render_template('500.html'), 500