from flask import request
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from wtforms.validators import Length

from app.models import User


class EditProfileForm(FlaskForm):
    """Edit User profile form."""
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username: str, *args, **kwargs) -> None:
        """Initialize class and store original username."""
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username: StringField) -> None:
        """Validate username on edit user profile."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('This username is already in use.')


class PostForm(FlaskForm):
    """Form to write new users posts."""
    post = TextAreaField(
        'Say something',
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField('Submit')


class EmptyForm(FlaskForm):
    """Filler forms with no business logic."""
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    """Form to submit user fulltext search."""
    class Meta:
        csrf = False

    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Form initialization."""
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super().__init__(*args, **kwargs)
