from flask import Blueprint, render_template, url_for, request, redirect, flash

from project import app, db
from project.messages.forms import MessageForm, DeleteForm
from project.users.models import User
from project.messages.models import Message
from project.helpers import login_required, not_loggedin_required, current_user_required

messages_blueprint = Blueprint(
    'messages', __name__, template_folder='templates')


# View all messages
@app.route('/messages')
def messages_index():
    return render_template('messages/messages_index.html', messages=Message.query.all()) 


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
    form.set_choices()
    return render_template('messages/new.html', user=User.query.get(user_id), form=form)


@messages_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
@current_user_required
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
@current_user_required
def edit_message(user_id, id):
    selected_message = Message.query.get(id)
    message_form = MessageForm(obj=selected_message)
    message_form.set_choices()
    return render_template('messages/edit.html', user=User.query.get(user_id), message=selected_message, message_form=message_form, delete_form=DeleteForm())
