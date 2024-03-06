"""Forms for user app."""

from wtforms import StringField, PasswordField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email


class RegisterUser(FlaskForm):
    """Form for registering user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class AddNoteForm(FlaskForm):
    """ Form for adding notes """
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])


class EditNoteForm(FlaskForm):
    """ Form for adding notes """
    title = StringField("Title")
    content = TextAreaField('Content')


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
