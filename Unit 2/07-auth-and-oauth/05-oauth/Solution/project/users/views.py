from flask import Blueprint, render_template, url_for, request, redirect, flash, session

from project import db, app, bcrypt, twitter_blueprint
from project.users.forms import UserForm, LoginForm, DeleteForm
from project.users.models import User, OAuth
from project.helpers import not_loggedin_required, current_user_required

from flask_login import login_required, login_user, logout_user, current_user
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# OAuth

@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(twitter_blueprint, token):
    if not token:
        flash("Failed to log in with Twitter.", category="error")
        return False

    resp = twitter_blueprint.session.get("account/settings.json")

    if not resp.ok:
        msg = "Failed to fetch user info from Twitter."
        flash(msg, category="error")
        return False

    twitter_info = resp.json()
    twitter_username = twitter_info['screen_name']

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=twitter_blueprint.name,
        twitter_username=twitter_username,
    )
    try:
        # Existing OAuth token in database
        oauth = query.one()
    except NoResultFound:
        # Create new OAuth token
        oauth = OAuth(
            provider=twitter_blueprint.name,
            twitter_username=twitter_username,
            token=token,
        )

    # If the token is associated with a user (?), log the user in
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Twitter.")
    else:
        """
        # Successful OAuth authentication without adding OAuth to existing non-OAuth accounts
        # Create a new local user account for this user
        user = User(
            first_name=twitter_username,
            # Less secure, but no username is generated, so on its own password cannot be used to log in
            password='password' 
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Twitter.")
        """

        # If user account already exists but there is no associated OAuth token
        if current_user.is_authenticated:
            oauth.user = current_user
            db.session.add(oauth)
            db.session.commit()
            flash("Successfully linked Twitter account.")
        else:
            # Create a new local user account for this user
            user = User(
                first_name=twitter_username,
                # Less secure, but no username is generated, so on its own password cannot be used to log in
                password='password'
            )
            # Associate the new local user account with the OAuth token
            oauth.user = user
            # Save and commit our database models
            db.session.add_all([user, oauth])
            db.session.commit()
            # Log in the new local user account
            login_user(user)
            flash("Successfully signed in with Twitter.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# Authentication


@users_blueprint.route('/signup', methods=["GET", "POST"])
@not_loggedin_required
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['first_name'], form.data['last_name'],
                            form.data['username'], form.data['password'])
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
@login_required
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
            selected_user.password = bcrypt.generate_password_hash(
                request.form['password']).decode('UTF-8')
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
@login_required
@current_user_required
def edit(id):
    selected_user = User.query.get(id)
    user_form = UserForm(obj=selected_user)
    return render_template('users/edit.html', user=selected_user, user_form=user_form, delete_form=DeleteForm())
