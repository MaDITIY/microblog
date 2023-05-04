from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm
from app.auth.forms import RegistrationForm
from app.auth.forms import ResetPasswordForm
from app.auth.forms import ResetPasswordRequestForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_instance = User.query.filter_by(username=form.username.data).first()
        if user_instance is None or not user_instance.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user_instance, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_instance = User.query.filter_by(email=form.email.data).first()
        if user_instance:
            send_password_reset_email(user_instance)
        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user_instance = User.verify_reset_password_token(token)
    if not user_instance:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_instance.set_password(form.password.data)
        db.session.commit()
        flash('Your password successfully reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
