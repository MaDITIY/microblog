from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from app.models import User


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[
            DataRequired(), 
            EqualTo('password')
        ],
    )
    submit = SubmitField('Register')

    def validate_username(self, username: StringField) -> None:
        """Validate username field."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already in use.')

    def validate_email(self, email: StringField) -> None:
        """Validate email field."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already in use.')


class ResetPasswordRequestForm(FlaskForm):
    """Form to request password reset email."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """Form to reset password."""
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[
            DataRequired(), 
            EqualTo('password')
        ],
    )
    submit = SubmitField('Reset Password')
