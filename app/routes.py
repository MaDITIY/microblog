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
from app.forms import PostForm
from app.forms import RegistrationForm
from app.models import Post
from app.models import User


@app.before_request
def before_request():
    """Before request executions."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts_paginator = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        max_per_page=app.config['MAX_POSTS_PER_PAGE'],
        error_out=False,
    )
    next_page_url = url_for('index', page=posts_paginator.next_num) \
        if posts_paginator.has_next else None
    prev_page_url = url_for('index', page=posts_paginator.prev_num) \
        if posts_paginator.has_prev else None
    posts = posts_paginator.items
    return render_template(
        'index.html',
        title='Explore',
        form=form,
        posts=posts,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
    )


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts_paginator = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        max_per_page=app.config['MAX_POSTS_PER_PAGE'],
        error_out=False,
    )
    next_page_url = url_for('index', page=posts_paginator.next_num) \
        if posts_paginator.has_next else None
    prev_page_url = url_for('index', page=posts_paginator.prev_num) \
        if posts_paginator.has_prev else None
    posts = posts_paginator.items
    return render_template(
        'index.html',
        title='Explore',
        posts=posts,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
    )


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
    page = request.args.get('page', 1, type=int)
    posts_paginator = user_instance.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,
        max_per_page=app.config['MAX_POSTS_PER_PAGE'],
        error_out=False,
    )
    next_page_url = url_for('user', username=username, page=posts_paginator.next_num) \
        if posts_paginator.has_next else None
    prev_page_url = url_for('user', username=username, page=posts_paginator.prev_num) \
        if posts_paginator.has_prev else None
    posts = posts_paginator.items
    return render_template(
        'user.html',
        user=user_instance,
        posts=posts,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
    )


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
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


@app.route('/follow/<username>')
@login_required
def follow(username):
    user_instance = User.query.filter_by(username=username).first()
    if user_instance is None:
        flash(f'User {username} not found')
        return redirect(url_for('index'))
    if user_instance == current_user:
        flash(f'You can\'t follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user_instance)
    db.session.commit()
    flash(f'You\'re now following {username}')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user_instance = User.query.filter_by(username=username).first()
    if user_instance is None:
        flash(f'User {username} not found')
        return redirect(url_for('index'))
    if user_instance == current_user:
        flash(f'You can\'t unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user_instance)
    db.session.commit()
    flash(f'You don\'t follow {username} anymore.')
    return redirect(url_for('user', username=username))
