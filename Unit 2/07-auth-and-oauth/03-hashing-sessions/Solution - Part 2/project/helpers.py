from project import app
from project.users.models import User
from flask import redirect, url_for, session, flash, g
from functools import wraps


# Make g.current_user available to all views
@app.before_request
def current_user():
    if session.get('user_id'):
        g.current_user = User.query.get(session['user_id'])
    else:
        g.current_user = None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please log in first")
            return redirect(url_for('users.login'))
        return fn(*args, **kwargs)
    return wrapper


def not_loggedin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            flash("You are logged in already")
            return redirect(url_for('users.users'))
        return fn(*args, **kwargs)
    return wrapper


def current_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        correct_id = kwargs.get('user_id') or kwargs.get('id')
        if correct_id != session.get('user_id'):
            flash("Not Authorized")
            return redirect(url_for('users.users'))
        return fn(*args, **kwargs)
    return wrapper
