from flask import (Blueprint, render_template, url_for, request, redirect,
                   flash, request, session, g)
from project.users.forms import UserForm, DeleteForm
from project.users.models import User
from project import db
from sqlalchemy.exc import IntegrityError
from functools import wraps

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

# Authorization and session helper code


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please log in first")
            return redirect(url_for('users.login'))
        return fn(*args, **kwargs)
    return wrapper


def ensure_correct_user(fn):
    # Make sure we preserve the __name__, and __doc__ values for our decorator
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # In the params we have something called id, is it the same as the user logged in?
        if kwargs.get('id') != session.get('user_id'):
            # If not, redirect them back home
            flash("Not Authorized")
            return redirect(url_for('users.welcome'))
        # Otherwise, move on with all the arguments passed in!
        return fn(*args, **kwargs)
    return wrapper


@users_blueprint.before_request
def current_user():
    if session.get('user_id'):
        g.current_user = User.query.get(session['user_id'])
    else:
        g.current_user = None


# Authentication


@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            flash("Invalid submission. Please try again.")
            return render_template('signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)


@users_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(
                form.data['username'], form.data['password'])
            if user:
                session['user_id'] = user.id
                flash("You've successfully logged in!")
                return redirect(url_for('users.welcome'))
        flash("Invalid credentials. Please try again.")
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been signed out.')
    return redirect(url_for('users.login'))


@users_blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', username=g.current_user.username)


# Authorization


@users_blueprint.route('/', methods=["GET", "POST"])
def users():
    if request.method == "POST":
        form = UserForm(request.form)
        if form.validate():
            new_user = User(request.form["first_name"],
                            request.form["last_name"])
            db.session.add(new_user)
            db.session.commit()
            flash("User Created!")
        else:
            flash("Form Error: User Not Created")
            return render_template('new.html', form=form)
    return render_template('index.html', users=User.query.all())


@users_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    selected_user = User.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        user_form = UserForm(request.form)
        if user_form.validate():
            selected_user.username = request.form['username']
            selected_user.password = request.form['password']
            db.session.add(selected_user)
            db.session.commit()
            flash("User Updated!")
            return redirect(url_for('users.users'))
        else:
            flash("Form Error: User Not Updated")
            return render_template('edit.html', user=selected_user,
                                   user_form=user_form, delete_form=DeleteForm())
    if request.method == b"DELETE":
        delete_form = DeleteForm(request.form)
        if delete_form.validate():
            db.session.delete(selected_user)
            db.session.commit()
            flash("User Deleted!")
            return redirect(url_for('users.users'))
        else:
            flash("Form Error: User Not Deleted")
            return redirect(url_for('users.users'))
    return render_template('show.html', user=selected_user)


@users_blueprint.route('/<int:id>/edit', methods=["GET"])
@ensure_correct_user
def edit(id):
    selected_user = User.query.get(id)
    user_form = UserForm(obj=selected_user)
    return render_template('edit.html', user=selected_user, user_form=user_form,
                           delete_form=DeleteForm())
