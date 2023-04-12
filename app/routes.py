# -*- coding: utf-8 -*-
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Dzianis'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}'
        )
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
