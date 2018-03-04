__author__ = 'Piotr Dyba'

from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.types import Integer, String, Boolean, JSON

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
    recipes = relationship('Recipe', backref='user', lazy=True)

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
    title = Column(String(250), default='')
    time_needed = Column(Integer, default=15)
    ingredients = Column(String(5000), default='')
    # ingredients = Column(JSON, default='')
    steps = Column(String(5000), default='')
    is_public = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
