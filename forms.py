"""Forms for user app."""

from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email

class RegisterUser(FlaskForm):
    """Form for registering user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(),Email()])
    first_name =  StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])