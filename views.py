#!/usr/bin/env python
# encoding: utf-8
from flask import request, redirect, flash, url_for, render_template
from main import app
from main import db
from main import bcrypt
from main import lm
from models import User
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if not request.form['email'] or not request.form['password'] :
        flash('Please fill in all the fields', 'danger')
        return redirect(url_for('register'))
    else:
        email = request.form['email']
        db_user = User.query.filter_by(email=request.form['email']).count()
        if db_user != 0:
            flash('User is already registered', 'danger')
            return redirect(url_for('login'))
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered', 'success')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('info'))
        return render_template('login.html')
    if not request.form['email'] or not request.form['password'] :
        flash('Please fill in all the fields', 'danger')
        return redirect(url_for('login'))
    form_email = request.form['email']
    form_pass = request.form['password']
    db_user = User.query.filter_by(email=form_email.lower()).first()
    if db_user is None or not bcrypt.check_password_hash(db_user.password, form_pass):
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login'))
    login_user(db_user)
    flash('Logged in successfully.', 'success')
    app.logger.debug('Logged in user %s', db_user.email)
    return redirect(url_for('info'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('info'))

@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return render_template('secret.html')

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

