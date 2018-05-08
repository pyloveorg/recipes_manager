__author__ = 'Piotr Dyba'

from sqlalchemy import create_engine
from main import db, bcrypt
import models


def db_start():
    create_engine('sqlite:///tmp/test.db', convert_unicode=True)
    db.create_all()
    db.session.commit()
    user = models.User(
        password=bcrypt.generate_password_hash('password').decode('utf-8'),
        email='amm.nowak@gmail.com',
        admin=True
    )

    user2 = models.User(
        password=bcrypt.generate_password_hash('password').decode('utf-8'),
        email='matisnape@wp.pl',
        admin=True
    )
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()


    recipe = models.Recipe(
        title="Private recipe user1",
        ingredients="Some ingredients",
        time_needed=15,
        steps="some steps",
        status='Private',
        user_id=user.id,
        average_score=None
    )
    recipe2 = models.Recipe(
        title="Public recipe user1",
        ingredients="Some ingredients",
        time_needed=15,
        steps="some steps",
        status='Public',
        user_id=user.id,
        average_score=5.0
    )
    recipe3 = models.Recipe(
        title="Private recipe user2",
        ingredients="Some ingredients",
        time_needed=15,
        steps="some steps",
        status='Private',
        user_id=user2.id,
        average_score=None
    )
    recipe4 = models.Recipe(
        title="Public recipe user2",
        ingredients="Some ingredients",
        time_needed=15,
        steps="some steps",
        status='Public',
        user_id=user2.id,
        average_score=3.0
    )
    db.session.add(recipe)
    db.session.add(recipe2)
    db.session.add(recipe3)
    db.session.add(recipe4)
    db.session.commit()

    vote1 = models.Vote(
        value = 1,
        user_id = user.id,
        recipe_id = recipe3.id
   )
    db.session.add(vote1)
    db.session.commit()


if __name__ == '__main__':
    db_start()
