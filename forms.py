"""Forms for user app."""

from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired


class RegisterUser(FlaskForm):
    """Form for registering user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """ Form for logging in a user """
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
