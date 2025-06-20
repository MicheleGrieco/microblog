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