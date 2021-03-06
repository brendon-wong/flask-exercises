from flask import Blueprint, render_template, url_for, request, redirect, flash

from solution import db
from solution.messages.forms import MessageForm, DeleteForm
from solution.users.models import User
from solution.messages.models import Message

messages_blueprint = Blueprint(
    'messages', __name__, template_folder='templates')


# See all messages for user
@messages_blueprint.route('/', methods=["GET", "POST"])
def messages(user_id):
    if request.method == "POST":
        form = MessageForm(request.form)
        if form.validate():
            new_message = Message(request.form["content"], user_id)
            db.session.add(new_message)
            db.session.commit()
            flash("Message Created!")
        else:
            flash("Form Error: Message Not Created")
            return render_template('messages/new.html', user=User.query.get(user_id), form=form)
    return render_template('messages/index.html', user=User.query.get(user_id))


@messages_blueprint.route('/new', methods=["GET"])
def new_message(user_id):
    form = MessageForm()
    return render_template('messages/new.html', user=User.query.get(user_id), form=form)


@messages_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show_message(user_id, id):
    selected_message = Message.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        message_form = MessageForm(request.form)
        if message_form.validate():
            selected_message.content = request.form['content']
            db.session.add(selected_message)
            db.session.commit()
            flash("Message Updated!")
            return redirect(url_for('messages.messages', user_id=user_id))
        else:
            flash("Form Error: Message Not Updated")
            return render_template('messages/edit.html', user=User.query.get(user_id), message=selected_message, message_form=message_form, delete_form=DeleteForm())
    if request.method == b"DELETE":
        delete_form = DeleteForm(request.form)
        if delete_form.validate():
            db.session.delete(selected_message)
            db.session.commit()
            flash("Message Deleted!")
            return redirect(url_for('messages.messages', user_id=user_id))
        else:
            flash("Form Error: Message Not Deleted")
            return redirect(url_for('messages.messages', user_id=user_id))
    return render_template('messages/show.html', user=User.query.get(user_id), message=selected_message)


@messages_blueprint.route('/<int:id>/edit', methods=["GET"])
def edit_message(user_id, id):
    selected_message = Message.query.get(id)
    message_form = MessageForm(obj=selected_message)
    return render_template('messages/edit.html', user=User.query.get(user_id), message=selected_message, message_form=message_form, delete_form=DeleteForm())
