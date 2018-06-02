from flask import Blueprint, render_template, url_for, request, redirect, flash

from project import db, app, bcrypt
from project.users.forms import UserForm, LoginForm, DeleteForm
from project.users.models import User
from project.helpers import not_loggedin_required, current_user_required

from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# Authentication


@users_blueprint.route('/signup', methods=["GET", "POST"])
@not_loggedin_required
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['first_name'], form.data['last_name'], form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
            # Log user in after registration
            login_user(new_user)
        except IntegrityError as e:
            flash("Username already taken")
            return render_template('users/signup.html', form=form)
        flash('User Created!')
        return redirect(url_for('users.users'))
    return render_template('users/signup.html', form=form)


@users_blueprint.route('/login', methods=["GET", "POST"])
@not_loggedin_required
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(
                form.data['username'], form.data['password'])
            if user:
                login_user(user)
                flash("You are now logged in!")
                return redirect(url_for('users.users'))
        flash("Invalid Credentials")
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out!')
    return redirect(url_for('users.login'))


# Views


@users_blueprint.route('/', methods=["GET", "POST"])
def users():
    return render_template('users/index.html', users=User.query.all())


@users_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
@current_user_required
def show(id):
    selected_user = User.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        user_form = UserForm(request.form)
        if user_form.validate():
            selected_user.first_name = request.form['first_name']
            selected_user.last_name = request.form['last_name']
            selected_user.username = request.form['username']
            selected_user.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
            db.session.add(selected_user)
            db.session.commit()
            flash("User Updated!")
            return redirect(url_for('users.users'))
        else:
            flash("Form Error: User Not Updated")
            return render_template('users/edit.html', user=selected_user, user_form=user_form, delete_form=DeleteForm())
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
    return render_template('users/show.html', user=selected_user)


@users_blueprint.route('/<int:id>/edit', methods=["GET"])
@current_user_required
def edit(id):
    selected_user = User.query.get(id)
    user_form = UserForm(obj=selected_user)
    return render_template('users/edit.html', user=selected_user, user_form=user_form, delete_form=DeleteForm())
