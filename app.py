"""Flask app for Notes"""
import os
from flask import Flask, request, render_template, redirect, session
from models import db, User, connect_db
from forms import RegisterUser, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///user_notes')
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

        new_user = User.register(
            username=username,
            pwd=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect(f"/users/{new_user.username}")

    else:

        return render_template('new_user_form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Displays login user form. If successful, processes the login request.
    Accepts: username and password from form."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, pwd=password)

        if user:
            session["username"] = user.username

            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Wrong username or password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user(username):

    if 'username' not in session:
        return redirect("/login")

    else:
        user = User.query.get_or_404(username)

        return render_template("user_info.html", user=user)
