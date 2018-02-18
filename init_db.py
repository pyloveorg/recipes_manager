__author__ = 'Piotr Dyba'

from sqlalchemy import create_engine
from main import db, bcrypt
import models


def db_start():
    create_engine('sqlite:///tmp/test.db', convert_unicode=True)
    db.create_all()
    db.session.commit()
    user = models.User()
    user.username = "ania"
    user.password = bcrypt.generate_password_hash('password').decode('utf-8')

    user.email = 'amm.nowak@gmail.com'
    user.admin = True
    user.poweruser = True
    db.session.add(user)
    db.session.commit()



if __name__ == '__main__':
    db_start()
