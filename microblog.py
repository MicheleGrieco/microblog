"""
Module Name: microblog.py
Author: Michele Grieco
Created: 2025-06-12
Description:
    This module defines the Flask shell context for the application.
    It allows you to access the database and models directly in the Flask shell.
    The `make_shell_context` function returns a dictionary that will be used to populate the shell context.
    This allows you to use the database and models without needing to import them manually in the shell.

Usage:
    This module is imported by the main application and is used to set up the Flask shell context.
    When you run `flask shell`, this context will be available, allowing you to interact with the database and models directly.
"""

import sqlalchemy as sa
import sqlalchemy.orm as so
# A Python script at the top-level that defines the Flask application instance.
from app import app, db # A single line that imports the application instance and the database
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    """
    Returns a dictionary that will be used to populate the shell context.
    This allows you to access the database and models directly in the Flask shell.
    The keys of the dictionary are the names you will use in the shell, and the values are the objects you want to access.
    For example, you can access the database with `db` and the User model with `User`.
    This function is automatically called when you run `flask shell`.    
    """
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}