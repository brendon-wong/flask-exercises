from flask import Blueprint, render_template, url_for, request, redirect, flash

from solution import db
from solution.users.forms import UserForm, DeleteForm
from solution.users.models import User

users_blueprint = Blueprint('users', __name__, template_folder='templates')


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
            return render_template('users/new.html', form=form)
    return render_template('users/index.html', users=User.query.all())


@users_blueprint.route('/new', methods=["GET"])
def new():
    form = UserForm()
    return render_template('users/new.html', form=form)


@users_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    selected_user = User.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        user_form = UserForm(request.form)
        if user_form.validate():
            selected_user.first_name = request.form['first_name']
            selected_user.last_name = request.form['last_name']
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
def edit(id):
    selected_user = User.query.get(id)
    user_form = UserForm(obj=selected_user)
    return render_template('users/edit.html', user=selected_user, user_form=user_form, delete_form=DeleteForm())
