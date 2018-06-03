from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps


def not_loggedin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are logged in already")
            return redirect(url_for('users.users'))
        return fn(*args, **kwargs)
    return wrapper


def current_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        correct_id = kwargs.get('user_id') or kwargs.get('id')
        if correct_id != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.users'))
        return fn(*args, **kwargs)
    return wrapper
