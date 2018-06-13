#!/usr/bin/env python
# encoding: utf-8
from flask import request, redirect, flash, url_for, render_template
from main import app, db
from main import bcrypt
from main import lm
from models import User, Recipe
from flask_login import current_user, login_user, logout_user, login_required
from forms import RegistrationForm, LoginForm

@app.route('/', methods=['GET'])
def index():
    top_recipes = Recipe.query \
        .filter(Recipe.status == "Public", Recipe.average_score != None) \
        .order_by(Recipe.average_score.desc(), Recipe.title.asc()) \
        .limit(10) \
        .all()

    top_ids = [recipe.id for recipe in top_recipes]

    worst_recipes = Recipe.query\
        .filter(Recipe.status == "Public", Recipe.average_score!=None, Recipe.id.notin_(top_ids))\
        .order_by(Recipe.average_score.asc(), Recipe.title.asc())\
        .limit(10)\
        .all()

    latest_recipes = Recipe.query\
        .filter(Recipe.status == "Public", Recipe.date_added!=None)\
        .order_by(Recipe.date_added.desc(), Recipe.title.asc())\
        .limit(10)\
        .all()
    return render_template('index.html', top_recipes=top_recipes, worst_recipes=worst_recipes, latest_recipes=latest_recipes)

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('accounts/register.html', form=form)
    if form.validate():
        email = form.email.data
        db_user = User.query.filter_by(email=email).count()
        if db_user != 0:
            flash('User is already registered', 'danger')
            return redirect(url_for('login'))
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered', 'success')
        return redirect(url_for('login'))
    flash('There are some problems here', 'danger')
    return render_template('accounts/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('info'))
        return render_template('accounts/login.html', form=form)
    if form.validate():
        form_email = form.email.data
        form_pass = form.password.data
        db_user = User.query.filter_by(email=form_email.lower()).first()
        if db_user is None or not bcrypt.check_password_hash(db_user.password, form_pass):
            flash('Invalid username or password. Try again?', 'danger')
            return redirect(url_for('login'))
        login_user(db_user)
        flash('Logged in successfully.', 'success')
        app.logger.debug('Logged in user %s', db_user.email)
        return redirect(url_for('all_recipes'))
    flash('Please fill in all the fields', 'danger')
    return render_template('accounts/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('all_recipes'))

@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return render_template('secret.html')

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

   

