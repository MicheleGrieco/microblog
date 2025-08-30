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
    """
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
