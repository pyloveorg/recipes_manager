__author__ = 'Piotr Dyba'

from datetime import datetime

from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.types import Integer, String, Boolean, JSON, Float, DateTime

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
    recipes = relationship('Recipe', backref='user', cascade='delete', lazy=True)
    votes = relationship('Vote', backref='user', cascade='delete', lazy=True)

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
    __searchable__ = ['title']

    id = Column(Integer, autoincrement=True, primary_key=True)
    date_added = Column(DateTime, default=datetime.now)
    title = Column(String(250), default='')
    time_needed = Column(Integer, default=15)
    ingredients = Column(String(5000), default='')
    # ingredients = Column(JSON, default='')
    steps = Column(String(5000), default='')
    status = Column(String, default='Public', nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    votes = relationship('Vote', backref='recipe', cascade='delete', lazy=True)
    average_score = Column(Float)

    def calculate_average(self):
        values = [vote.value for vote in self.votes]
        self.average_score = sum(values) / len(values)


class Vote(db.Model):
    """
    Vote Model
    """
    __tablename__ = 'votes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)








