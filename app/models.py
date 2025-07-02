"""
Module Name: models.py
Author: Michele Grieco
Created: 2025-06-19
Description:
    This module defines the database models for the Flask application.
    It includes the User and Post models, which represent users and their posts in the application.
    The User model includes methods for password hashing and Gravatar avatar generation.
    The Post model represents user-generated content.

Usage:
    This module is imported by the main application and is used to define the database schema.
    The models are used to interact with the database, allowing for user authentication and post management.
"""

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa # general purpose database functions and classes such as types and query building helpers
import sqlalchemy.orm as so # support for using models
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

# Safe implementations for user login requirements (is_authenticated, is_active, is_anonymous, get_id())
from flask_login import UserMixin

# Auxiliary table representing followers (not declared as a model)
followers = sa.Table('followers', 
                     db.metadata, 
                     sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
                     sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
                     )

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # 'Optional' attribute for NULL values
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author') # WriteOnlyMapped defines posts as a collection type with Post objects inside
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    following: so.WriteOnlyMapped['User'] = so.relationship(secondary=followers, # Configures the association table
                                                            primaryjoin=(followers.c.follower_id ==id),
                                                            secondaryjoin=(followers.c.followed_id == id),
                                                            back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(secondary=followers, # Configures the association table
                                                            primaryjoin=(followers.c.followed_id == id),
                                                            secondaryjoin=(followers.c.follower_id == id),
                                                            back_populates='following')
    
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
    
    def is_following(self, user):
        """
        Checks if the user is following another user.
        :param user: The user to check if the current user is following.
        :type user: User
        :return: True if the current user is following the specified user, False otherwise.
        :rtype: bool
        """
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None
    
    def follow(self, user):
        """
        Follows another user.
        This method adds the specified user to the current user's following list.
        :param user: The user to follow.
        :type user: User
        :return: None
        :note: If the user is already being followed, this method does nothing.
        """
        if not self.is_following(user):
            self.following.add(user)
            
    def unfollow(self, user):
        """
        Unfollows another user.
        This method removes the specified user from the current user's following list.
        :param user: The user to unfollow.
        :type user: User
        :return: None
        :note: If the user is not being followed, this method does nothing.
        """
        if self.is_following(user):
            self.following.remove(user)        
    
    def followers_count(self):
        """
        Returns the number of followers for the user.
        This method counts the number of users who are following the current user.
        :return: The number of followers.
        :rtype: int
        :note: This method executes a query to count the number of entries in the followers association table
        for the current user.
        """
        # Whenever a query is included as part of a larger query,
        # SQLAlchemy requires the inner query to be converted to a sub-query by calling the subquery() method.
        query = sa.select(sa.func.count()).select_from(self.followers.select().subquery())
        return db.session.scalar(query)
    
    def following_count(self):
        """
        Returns the number of users that the current user is following.
        This method counts the number of users that the current user is following.
        :return: The number of users that the current user is following.
        :rtype: int
        :note: This method executes a query to count the number of entries in the following association table
        for the current user.
        """
        # Whenever a query is included as part of a larger query,
        # SQLAlchemy requires the inner query to be converted to a sub-query by calling the subquery() method.
        query = sa.select(sa.func.count()).select_from(self.following.select().subquery())
        return db.session.scalar(query)
    
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