"""
Module name: microblog.py
Author: Michele Grieco
Description:
    Entry point for the Flask microblog application.
    Sets up the application context and shell context for interactive use.
Usage:
    - Run the application using Flask CLI.
    - Access database models and SQLAlchemy objects in the shell context.
"""

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Post

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Provide a shell context for the Flask application.
    This function returns a dictionary of database objects and models to be
    available in the shell.
    :return: Dictionary with SQLAlchemy and model references
    """
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
