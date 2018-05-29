## Password Hashing with Bcrypt in Flask

### Objectives:

By the end of this chapter, you should be able to:

*   Compare and contrast authentication and authorization
*   Use bcrypt to securely hash passwords
*   Explain what a `salt` and a `work factor` are

### Introduction

So far our applications have handled multiple resources, but we have not discussed an essential part of building web applications: authentication and authorization! Let's first define what these terms mean.

**Authentication** - making sure a user is who they say they are. The process of logging in is a prime example of authentication. In order to successfully log in, we need to make sure a user is who they say they are (by providing a correct username and password).

**Authorization** - making sure a user is allowed to access a route / resource. On Facebook, you are not "authorized" to delete **other** people's posts. On Github, you are not authorized to push to other people's repositories unless they "authorize" you.

Let's start with authentication and analyze the key parts of the process: signing up and logging in.

**Signing up** - make sure a user provides a unique identifier (username / email) and a password. Store that information in the database for when a user logs in

**Logging In** - first make sure that the user has provided a unique identifier (username / email) that exists. If that identifier exists, check to see if their password provided is the same one as in the database. If it is, log them in!

In the sign up process, we mention that we store a username and password that a user provides when saving them. This seems simple, but there is a **highly dangerous** security risk that we must always consider. When we accept the username and password, they come to the server as plain text, which means that if we were to store that information directly we would be storing our password in plain text.

So what's the problem here? Imagine if someone (a hacker, disgruntled employee or even another developer) got access to your database and every user's password was clearly visible. Not only would this be a terrible security breach for your application, but very commonly we use the same password for many different applications. So when storing passwords, we must always remember: **NEVER STORE PASSWORDS IN PLAIN TEXT.**

What we need to do is _hash_ a password before saving it to the database. You'll sometimes see hashing referred to as _one-way encryption_. This means that our goal isn't to ever decrypt the password: instead, we just want to make it difficult for someone to obtain a user's password even if they gain access to the database.

But if we don't know the user's password, how can we log them in? The trick is that when someone attempts to log in, we'll hash the password they type, and compare that hashed password to the value in the database. But we never decrypt anything. (You'll see more details of this in just a moment.)

Another type of encryption, which we won't be using, is _two-way encryption_. With two-way encryption, both parties know a secret key that they can use to decipher messages.

hen you are doing any kind of password hashing, you should use an industry established hashing algorithm. We will be using the `bcrypt` algorithm which is based off of the [Blowfish cipher](https://en.wikipedia.org/wiki/Blowfish_(cipher)).

### Hashing passwords with `bcrypt`

To get started using `bcrypt`, let's first create a virtual environment and install Flask. While `bcrypt` doesn't come natively in Flask, there is a `bcrypt` module designed for integration with Flask, called (unsurprisingly) `flask-bcrypt`:

~~~~
mkvirtualenv learn-auth
workon learn-auth
pip install flask flask-bcrypt ipython
createdb learn-auth
~~~~

Before building our app, let's explore how `bcrypt` works. Hop into `ipython` and run the following:

~~~~
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

pw_hash = bcrypt.generate_password_hash('secret')
bcrypt.check_password_hash(pw_hash, 'secret') #  True
bcrypt.check_password_hash(pw_hash, 'secret2') # False
pw_hash # should look like a long, incomprehensible byte literal!
~~~~

This is exactly how we will be storing our users' passwords and checking to see if they are correct!

### Structure of the hashed password

If you look at a password that's been hashed using `bcrypt`, it should look like a bunch of characters jumbled together. However, there is a structure in this hashed password that it's helpful to know about. Let's look at an example:

~~~~
b'$2b$12$3cy0jD1AfgcT0ipGL1UhquBZXvAxUwRrdG90Gi951AcxIXm2F2gMK'
# prefix = 2b
# work factor = 12
# salt = 3cy0jD1AfgcT0ipGL1Uhqu
# hash = BZXvAxUwRrdG90Gi951AcxIXm2F2gMK
~~~~

We won't go into too much detail about these components of the byte literal, but it is worth knowing a bit about these different pieces. The hashed password is actually just the last 31 characters of the byte literal (`BZXvAxUwRrdG90Gi951AcxIXm2F2gMK`). The rest of the components give you information about _how_ the original password was hashed.

The prefix is not terribly important: it simply indicates that `bcrypt` was used to encrypt the password, as opposed to some other encryption algorithm. In this case the prefix is `2b`, but for `bcrypt` you might also see `2a` or `2y` as the prefix.

Next comes the work factor. Roughly speaking, this measures how long it takes to perform the encryption. One benefit to using a good hashing algorithm is that it can prevent _brute force attacks_, whereby an attacker simply tries thousands or even millions of passwords in quick succession. The more time it takes to hash the passwords and perform the check, the less effective a brute force attack becomes. However, there's also a tradeoff here: the higher the work factor, the better the hashing, but the worse the user experience. Imagine if it took several minutes to log in to a website because of the time spent hashing the password that the user typed in!

Finally, you can think of the `salt` as a randomly generated string that's used to provide a degree of randomness into the hashing process. The salt is combined with the original password to generate the hash. The salt is stored along with the hash because if you want to check that the user has provided the right password when they attempt to log in, you need to know what salt was originally used to hash the encrypted password that's stored in the database.

This is also why when you hash the same string twice, you'll get different output values from `bcrypt`! Because of the salt, even people who have the same passwords will have different hashes in the database.

~~~~
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

hash1 = bcrypt.generate_password_hash('secret')
hash2 = bcrypt.generate_password_hash('secret')

hash1 == hash2 # False - check out the hashes, they'll have different values!
hash3 = bcrypt.generate_password_hash('secret', 17) # the second argument lets us increase/decrease the work factor. Default value is 12.
~~~~

For more details on Bcrypt, you can check out [this](https://en.wikipedia.org/wiki/Bcrypt) article. If you're curious about the work factor specifically, [this](https://wildlyinaccurate.com/bcrypt-choosing-a-work-factor/) blog post digs into performance a bit.

### Creating an application that allows a user to log in

Now that we have an idea of how to secure our passwords, let's build a Flask application that contains two forms: signup and login. We will securely store the user's information and authenticate them when they submit the signup form. If they successfully log in, we will redirect them to a simple page that says "You are logged in!"

To begin, let's set up our application so it follows our new structure for Flask applications. From the `learn-auth` directory, we need to create the following files and folders:

~~~~
touch app.py
mkdir project
mkdir project/{users,templates}
mkdir project/users/templates
touch project/users/templates/{signup,login,welcome}.html
touch project/users/{forms,models,views}.py
touch project/templates/base.html
touch project/__init__.py
pip install psycopg2 flask-sqlalchemy flask-wtf flask-migrate flask-bcrypt
~~~~

That's a fair amount of setup, but with practice the process should become more familiar. Let's put some initial setup into our `project/__init__.py`:

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret' # bad practice in general, but we'll live with it for now
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from project.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
~~~~

Of course, we don't have a users blueprint yet, so let's work on that next. With `db` and `bcrypt` defined, let's create our `User` model in `project/users/models.py`:

~~~~
from project import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
~~~~

(The decoding on the password just ensures that our passwords are stored in the database with the proper character encoding.)

We'll also need a form for signing up and logging in. Here's our `project/users/forms.py`:

~~~~
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
~~~~

Next we need to work on `project/users/views.py`. Here's some starter code (we'll unpack it below):

~~~~
from flask import redirect, render_template, request, url_for, Blueprint
from project.users.forms import UserForm
from project.users.models import User
from project import db,bcrypt

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

@users_blueprint.route('/signup', methods =["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return render_template('signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)

@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        found_user = User.query.filter_by(username = form.data['username']).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, form.data['password'])
            if authenticated_user:
                return redirect(url_for('users.welcome'))
    return render_template('login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
~~~~

The bulk of the logic comes inside of the `signup` and `login` methods. Let's take a look at `signup` first. Here's what happens:

1.  If the user has submitted a form (i.e. made a POST request), we first validate the form. If the user has submitted a GET request, we will render the `signup` page.
2.  If the form is validated, we try to add the new user to the database (note: the encryption is handled in the `User` model, so we don't need to explicitly refer to `bcrypt` here).
3.  If there's an error in creating the user, or a problem with form validation, the user is sent back to the signup page. Otherwise, if the user is successfully created, the user is sent to the login page.

Similarly, here's what happens inside of `login`:

1.  If the user has submitted a form (i.e. made a POST request), we first validate the form. If the user has submitted a GET request, we will render the `login` page.
2.  If the form is valid, we search our database for a user matching the email address in the form. If no match is found, we send the user back to the `login` page.
3.  If a match is found, we check to see whether the user provided the correct password.
4.  If the user provided the correct password, we welcome the user in. Otherwise, we go back to the `login` page.

If you look at the following code:

~~~~
found_user = User.query.filter_by(username = form.data['username']).first()
    if found_user:
        authenticated_user = bcrypt.check_password_hash(found_user.password, form.data['password'])
            if authenticated_user:
~~~~

There is a nice option to refactor here, where we can move some of this logic into a method in our model. We could make a class method called authenticate which accepts a username and a password and implements the following logic above. By moving that logic to a model, we can delegate the responsibility of our "data" related logic to the model and reduce code in our controller.

Here's what that might look like:

~~~~
from project import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    # notice we are making a class method here since we will be invoking this using User.authenticate() 
    @classmethod
    # let's pass some username and some password 
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username = username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticated_user:
                return found_user # make sure to return the user so we can log them in by storing information in the session
        return False
~~~~

After moving authentication to the model, we can simplify our `login` function inside of `project/users/views` to use our new class method:

~~~~
@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        if User.authenticate(form.data['username'], form.data['password']):
            return redirect(url_for('users.welcome'))
    return render_template('login.html', form=form)
~~~~

We can also stop importing `bcrypt` inside of our views file - only the model needs it now!

With this, all of our server-side code is complete. Let's run a quick migration:

~~~~
flask db init
flask db migrate
flask db upgrade
~~~~

If you have any errors, try your best to debug them!

Let's now add our views. Let's keep things as simple as possible:

`project/templates/base.html`

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Authentication App</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
~~~~

`project/users/templates/signup.html`

~~~~
{% extends 'base.html' %}

{% block content %}

<form method="POST" action="{{url_for('users.signup')}}">
  {{ form.csrf_token }}
  <p>{{ form.username(placeholder="username") }}
    <span>
      {% if form.username.errors %}
        {% for error in form.username.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <p>
    {{ form.password(placeholder="password") }}
    <span>
      {% if form.password.errors %}
        {% for error in form.password.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <button type="submit">Sign Up!</button>
</form>

{% endblock %}
~~~~

`project/users/templates/login.html`

~~~~
{% extends 'base.html' %}

{% block content %}

<form method="POST" action="{{url_for('users.login')}}">
  {{ form.csrf_token }}
  <p>{{ form.username(placeholder="username") }}
    <span>
      {% if form.username.errors %}
        {% for error in form.username.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <p>
    {{ form.password(placeholder="password") }}
    <span>
      {% if form.password.errors %}
        {% for error in form.password.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <button type="submit">Log In!</button>
</form>

{% endblock %}
~~~~

`project/users/templates/welcome.html`

~~~~
{% extends 'base.html' %}

{% block content %}

<h1>You are logged in!</h1>

{% endblock %}
~~~~

Finally, let's complete our `app.py`:

~~~~
from project import app

if __name__ == '__main__':
    app.run(debug=True)
~~~~

Now you can run `python app.py` and confirm that the app works as expected. Things you should verify:

1.  You can't sign up without entering a username and a password.
2.  You can't sign up with a username that's already been taken.
3.  You can't log in with a username that's not in the database.
4.  You can't log in if you supply an invalid password.
5.  If you log in with the correct username and password, you get to the welcome page.
6.  Your database is storing encrypted passwords, not plain text passwords.

When you're ready, move on to [Authentication with Cookies and Sessions in Flask](/courses/intermediate-flask/cookies-sessions-flask)