# type: ignore
"""
Module name: models.py
Author: Michele Grieco
Description:
    Database models for the Flask microblog application.
    This module defines the User and Post models, as well as a many-to-many
    relationship for followers.
    The User model includes methods for password hashing, avatar generation,
    following/unfollowing users, and generating password reset tokens.
    The Post model includes a searchable mixin to enable full-text search
    capabilities using Elasticsearch.
Usage:
    - User: Represents a user in the application.
    - Post: Represents a blog post in the application.
    - SearchableMixin: Mixin class to add search capabilities to models.
"""

from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin:
    
    @classmethod
    def search(cls, expression, page, per_page) -> tuple[list, int]:
        """
        Search for records matching the given expression.
        :param expression: The search expression.
        :param page: The page number for pagination.
        :param per_page: The number of items per page.
        :return: A tuple containing the list of matching records and the total count.
        """
        ids, total = query_index(cls.__tablename__, expression, page, per_page) # type: ignore
        if total == 0:
            return [], 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        query = sa.select(cls).where(cls.id.in_(ids)).order_by(db.case(*when, value=cls.id)) # type: ignore
        return db.session.scalars(query), total
    
    @classmethod
    def before_commit(cls, session) -> None:
        """
        Store changes to be processed after the commit.
        :param session: The database session.
        :return: None
        """
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
    
    @classmethod
    def after_commit(cls, session):
        """
        Process changes after the commit to update the search index.
        :param session: The database session.
        :return: None
        """
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None
        
    @classmethod
    def reindex(cls):
        """
        Reindex all records of the model.
        :return: None
        """
        for obj in db.session.scalars(sa.select(cls)):
            add_to_index(cls.__tablename__, obj)

# Set up event listeners to handle before and after commit events
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

# Association table for followers relationship
followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password) # type: ignore

    def avatar(self, size) -> str:
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def follow(self, user) -> None:
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user) -> None:
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user) -> bool:
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self) -> Optional[int]:
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self) -> Optional[int]:
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)

    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            ))
            .group_by(Post) # type: ignore
            .order_by(Post.timestamp.desc())
        )

    def get_reset_password_token(self, expires_in=600) -> str:
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token) -> Optional['User']:
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)


@login.user_loader
def load_user(id) -> Optional[User]:
    return db.session.get(User, int(id))


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5))

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self) -> str:
        return '<Post {}>'.format(self.body)
