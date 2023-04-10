# -*- coding: utf-8 -*-
from flask import render_template

from app import app


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
