"""Flask app for Notes"""
import os
from flask import Flask, request, render_template, redirect
from models import db, User, connect_db
from forms import RegisterUser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///users')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"


@app.get('/')
def show_homepage():
    """Redirects to register."""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Shows form for user registration, and registers new user."""

    form = RegisterUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username,
                        hashed_password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        return redirect(f"/users/{new_user.username}")

    else:

        return render_template('new_user_form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Displays login user form. If successful, processes the login request.
    Accepts: username and password from form."""



