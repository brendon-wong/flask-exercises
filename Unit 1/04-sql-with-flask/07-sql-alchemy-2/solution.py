from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

# Create instance of Flask class, set custom template and static folder
app = Flask(__name__, template_folder="solution_templates",
            static_folder="solution_static")

# Configure Flask Modus
modus = Modus(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/users-messages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = "users"

    # Columns in table
    id = db.Column(db.Integer, primary_key=True)
    # 50 characters is a sensible default for the max length of first/last names
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    # Set a custom string representation of user objects
    def __repr__(self):
        return f"{self.first_name} {self.last_name}'s username is {self.username} and email is {self.email}"


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    # Set a custom string representation of message objects
    def __repr__(self):
        return f"User {self.user_id} wrote '{self.text}'"


@app.route('/', methods=["GET"])
def home():
    return redirect('users')


# Users


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "POST":
        new_user = User(request.form["first_name"], request.form["last_name"])
        db.session.add(new_user)
        db.session.commit()
        # return redirect(url_for('users'))
    return render_template('users/index.html', users=User.query.all())


@app.route('/users/new', methods=["GET"])
def new():
    return render_template('users/new.html')


@app.route('/users/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    selected_user = User.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        selected_user.first_name = request.form['first_name']
        selected_user.last_name = request.form['last_name']
        db.session.add(selected_user)
        db.session.commit()
        return redirect(url_for('users'))
    if request.method == b"DELETE":
        db.session.delete(selected_user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('users/show.html', user=selected_user)


@app.route('/users/<int:id>/edit', methods=["GET"])
def edit(id):
    return render_template('users/edit.html', user=User.query.get(id))


# Messages


# See all messages for user
@app.route('/users/<int:user_id>/messages', methods=["GET", "POST"])
def messages(user_id):
    if request.method == "POST":
        new_message = Message(request.form["content"], user_id)
        db.session.add(new_message)
        db.session.commit()
    return render_template('messages/index.html', user=User.query.get(user_id))


@app.route('/users/<int:user_id>/messages/new', methods=["GET"])
def new_message(user_id):
    return render_template('messages/new.html', user=User.query.get(user_id))


@app.route('/users/<int:user_id>/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show_message(user_id, id):
    selected_message = Message.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        selected_message.content = request.form['content']
        db.session.add(selected_message)
        db.session.commit()
        return redirect(url_for('messages', user_id=user_id))
    if request.method == b"DELETE":
        db.session.delete(selected_message)
        db.session.commit()
        return redirect(url_for('messages', user_id=user_id))
    return render_template('messages/show.html', user=User.query.get(user_id), message = selected_message)


@app.route('/users/<int:user_id>/messages/<int:id>/edit', methods=["GET"])
def edit_message(user_id, id):
    return render_template('messages/edit.html', user=User.query.get(user_id), message=Message.query.get(id))


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
