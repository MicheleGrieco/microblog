from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa # general purpose database functions and classes such as types and query building helpers
import sqlalchemy.orm as so # support for using models
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # safe implementations for user login requirements
from hashlib import md5

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # 'Optional' attribute for NULL values
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author') # WriteOnlyMapped defines posts as a collection type with Post objects inside
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    
    def avatar(self, size):
        """
        Generates a Gravatar URL for the user based on their email address.
        :param size: The size of the avatar image in pixels.
        :type size: int
        :return: A URL to the Gravatar image.
        :rtype: str
        :example: 'https://www.gravatar.com/avatar/abc123?d=identicon&s=128'
        :note: The email is converted to lowercase and hashed using MD5 to create a unique identifier for the Gravatar.
        :see: https://en.gravatar.com/site/implement/images/
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest() # needs to be lowercase and encoded in utf-8
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}' # 'd' is the default image type, 's' is the size of the image
    
    def __repr__(self):
        """
        Returns a string that includes the username of the user.
        This method is called when the object is printed or logged.
        
        :return: A string representation of the User object.
        :rtype: str
        :example: '<User john_doe>'
        :note: This method is useful for quickly identifying the user in logs or debugging output.
        :see: https://docs.python.org/3/reference/datamodel.html#object.__repr__
        """
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        """
        Sets the password for the user by hashing it.
        This method uses a secure hashing algorithm to store the password securely.
        :param password: The plaintext password to be hashed.
        :type password: str
        :return: None
        """
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.
        This method is used to verify a user's password during login.
        :param password: The plaintext password to check.
        :type password: str
        :return: True if the password matches, False otherwise.
        """
        match self.password_hash:
            case str():
                return check_password_hash(self.password_hash, password)
            case _:
                return False
    
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    
    def __repr__(self):
        """
        Returns a string that includes the body of the post.
        This method is called when the object is printed or logged.
        :return: A string representation of the Post object.
        :rtype: str
        :example: '<Post This is a sample post>'
        :note: This method is useful for quickly identifying the post in logs or debugging output.
        :see: https://docs.python.org/3/reference/datamodel.html#object.__repr__
        """
        return '<Post {}>'.format(self.body)
    
    
    
@login.user_loader
def load_user(id):
    """
    Loads a user from the database by their ID.
    The id can be an integer or a string, and it will be converted to an integer.
    :param id: The ID of the user to load.
    :type id: int or str
    :return: The User object if found, or None if not found.
    :rtype: User or None
    """
    return db.session.get(User, int(id))