"""Flask app for Notes"""
import os
from flask import Flask, request, render_template, redirect, session, flash
from models import db, User, Note, connect_db
from forms import RegisterUser, LoginForm, AddNoteForm, CSRFProtectForm, EditNoteForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///user_notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

USERNAME_IN_SESSION = 'username'


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

        session[USERNAME_IN_SESSION] = new_user.username

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
            session[USERNAME_IN_SESSION] = user.username

            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Wrong username or password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user(username):
    """show user info."""

    if USERNAME_IN_SESSION not in session:
        flash('You are not logged in.')
        return redirect("/login")

    if session[USERNAME_IN_SESSION] != username:
        current_user = username
        flash('You do not have access.')
        return redirect(f"/users/{current_user}")

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    return render_template("user_info.html", user=user, form=form)


@app.post('/logout')
def logout_user():
    """logs user out and redirects to index."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USERNAME_IN_SESSION, None)
        flash('You are now logged out.')
        return redirect('/')

    flash('You do not have access.')
    return redirect('/')


@app.delete('/users/<username>/delete')
def delete_user(username):
    """ Remove the user from the database. Log the user out and redirect to /
    """

    user = User.query.get_or_404(username)

    Note.query.filter(Note.owner_username == user.username).delete()

    db.session.delete(user)
    db.session.commit()

    return redirect('/')


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def display_add_notes_form(username):
    """ Display form to add notes """

    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(
            title=title,
            content=content,
            owner_username=username)

        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template('add_note.html', form=form)



@app.route('/notes/<note_id>/update', methods=["GET", "POST"])
def update_notes(note_id):
    """"Displays a form to edit user notes on page, and for making changes."""


    form = EditNoteForm()
    note = Note.query.get_or_404(note_id)

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data or note.title
        note.content = form.content.data or note.content

        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    return render_template('edit_note.html', form=form, note=note)


@app.post('/notes/<note_id>/delete')
def delete_note(note_id):
    """Delete user's current note."""

    note = Note.query.get_or_404(note_id)

    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{note.owner_username}")


