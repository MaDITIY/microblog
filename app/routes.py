# -*- coding: utf-8 -*-
from datetime import datetime

from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app import app
from app import db
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User


@app.before_request
def before_request():
    """Before request executions."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!',
        },
        {
            'author': {'username': 'Viktoryia'},
            'body': 'Let\'s have some fun!!!',
        },
        {
            'author': {'username': 'Nick'},
            'body': 'Hello world!!!',
        },
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_instance = User.query.filter_by(username=form.username.data).first()
        if user_instance is None or not user_instance.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user_instance, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_instance = User(username=form.username.data, email=form.email.data)
        user_instance.set_password(form.password.data)
        db.session.add(user_instance)
        db.session.commit()
        flash("Congratulations, you're now registered!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user_instance = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user_instance, 'body': 'Test post #1'},
        {'author': user_instance, 'body': 'Test post #2'},
    ]
    return render_template('user.html', user=user_instance, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
