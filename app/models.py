from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa # general purpose database functions and classes such as types and query building helpers
import sqlalchemy.orm as so # support for using models
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # 'Optional' attribute for NULL values
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author') # WriteOnlyMapped defines posts as a collection type with Post objects inside
    
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
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
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