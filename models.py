__author__ = 'Piotr Dyba'

from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean

from main import db


class User(db.Model, UserMixin):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    email = Column(String(200), unique=True)
    password = Column(String(200), default='')
    admin = Column(Boolean, default=False)

    def is_active(self):
        """
        Returns if user is active.
        """
        return self.active

    def is_admin(self):
        """
        Returns if user is admin.
        """
        return self.admin

class Recipe(db.Model):
    """
    Recipe Model
    """
    __tablename__ = 'recipe'
    id = Column(Integer, autoincrement=True, primary_key=True)
    is_public = Column(Boolean, default=True)
    title = Column(String(250), default='')
    time_needed = Column(Integer, default=15)
    ingredients = Column(String(1000), default='')
    steps = Column(String(5000), default='')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
