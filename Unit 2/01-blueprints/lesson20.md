### Objectives:

By the end of this chapter, you should be able to:

*   Explain what the MVC pattern is and why it's useful
*   Structure larger Flask applications using blueprints
*   Refactor previous applications to use a more scalable structure

### Blueprints

Our applications are getting a bit out of hand. Right now we are placing all of our configuration settings, database logic and routing logic inside of a single file, our `app.py`. Imagine what would happen if we had dozens of models and resources that we were doing CRUD on? We need a better system for organizing our code, and Flask gives us one! It's called `blueprints`.

Before we get into blueprints, let's discuss a very common pattern of structuring parts of a large application. It's called the **M**odel **V**iew **C**ontroller (or **MVC**) pattern, and it is prevalent in larger frameworks like Ruby on Rails.

### MVC

MVC is a design pattern for building web applications. Traditionally, your application is structured into three parts:

*   `Model` - a model is responsible for managing data storage, retrieval, and validation in an application. The models we have made in SQLAlchemy do just that!
    
*   `View` - the view is what a user sees. We should strive to minimize the amount of logic in our views as we want to keep them as simple as possible, and delegate logic to our controller.
    
*   `Controller` - the brains (or business logic) behind the operation. The controller is responsible for talking to the model when necessary and updating the view. The controller is where actions are actually processed and determines what data to retrieve from the Model, how to package it, and update the View with that data.
    

You can read much more about MVC summarized with legos [here](https://realpython.com/blog/python/the-model-view-controller-mvc-paradigm-summarized-with-legos/). For more attempts to explain the pattern in concrete terms, check out this [Quora question](https://www.quora.com/Whats-the-easiest-way-to-explain-RailsMVC-structure). You can also read more about the communication between the model, controller, and view [here](http://softwareengineering.stackexchange.com/questions/234116/model-view-controller-does-the-user-interact-with-the-view-or-with-the-controll).

### Getting started with our first blueprint

Now that we have an idea of what MVC is, we are going to break apart pieces of our application to adhere to this structure. This is going to make our folder structure a bit larger, but tremendously reduce the amount of code we have in our `app.py`. Let's create a new application and start with a single resource, `Owner`. Here is what our folder structure is going to look like:

~~~~
.
├── requirements.txt 
├── app.py # file to start the server
├── migrations # folder that contains our migrations
├── project # the root folder for all of our resources
    # the main file for defining our app variable and registering blueprints 
│   ├── __init__.py 
    # SQLAlchemy configuration (if you only have a few models you can put them in one single file)
│   ├── models.py
    # for CSS / JS / images and fonts
│   ├── static
    # templates for ALL other templates to inherit from
│   ├── templates
│   │   └── base.html
    # a folder for one resouce (other resources will look just like this)
│   └── owners
        # WTForms configuration
│       ├── forms.py
        # All templates specific to that resource
│       ├── templates
|       |   |---owners
|       |    # All templates specific to that resource
│       │       ├── index.html
│       │       ├── edit.html
│       │       ├── show.html
│       │       └── new.html
        # The controller for this resource. This is where our routes live
│       └── views.py
~~~~

### Necessary files

Now that we have this folder structure, let's start by creating a virtual environment

~~~~
mkvirtualenv flask-blueprints
workon flask-blueprints
createdb flask-blueprints
pip install flask psycopg2 flask-sqlalchemy flask-migrate flask-wtf flask-modus
~~~~

Now we need to set up our `project/__init__.py` file to configure flask:

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_migrate import Migrate

app = Flask(__name__)
modus = Modus(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-blueprints'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "THIS SHOULD BE HIDDEN!"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import a blueprint that we will create
from project.owners.views import owners_blueprint

# register our blueprints with the application
app.register_blueprint(owners_blueprint, url_prefix='/owners')

@app.route('/')
def root():
    return "HELLO BLUEPRINTS!"
~~~~

We are importing a blueprint that does not exist yet, so let's head to our `/project/owners/views.py` file and create a blueprint

~~~~
from flask import Blueprint  # we will import much more later

# let's create the owners_blueprint to register in our __init__.py
owners_blueprint = Blueprint(
    'owners',
    __name__,
    template_folder='templates'
)
~~~~

Next, let's create our model. Inside of our `project/models.py` let's create a model for an owner:

~~~~
from project import db

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
~~~~

Finally, let's import our newly created model in our `views.py`. You'll get a warning from your linter saying that you're importing something that you're not using; that's okay for now, we'll need to use the `Owner` model later on when we dig into the routing.

~~~~
from flask import Blueprint
from project.models import Owner

owners_blueprint = Blueprint(
  'owners',
  __name__,
  template_folder = 'templates'
)
~~~~

For now, since we've imported our Owner model, we can run our migrations. Let's create our migrations folder, pending migration and then run the migration.

~~~~
flask db init
flask db migrate
flask db upgrade
~~~~

Now we need to set up our `app.py` file to start the server:

~~~~
from project import app
~~~~

We should be able to run `flask run` and start a server! If you head to [http://localhost:5000](http://localhost:5000) we should see "HELLO BLUEPRINTS!". You also might be wondering what `project` is that we are importing. That is actually the `__init__.py` file inside of the project folder!

Before moving on, you may want to create a few owners inside of IPython so that you have some data to work with as we begin implementing full CRUD.

### Starting on CRUD

Let's make sure we first have a `project/templates/base.html` file:

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blueprints App</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
~~~~

### Index

Now let's build the route and view necessary to display our owners. We will be adding routes in our `project/owners/views.py` file. Remember, we will not be using a decorator of `@app`, we will be using our blueprint! So our decorator for the route will be `@owners_blueprint`, which is what we named the blueprint.

~~~~
from flask import redirect, render_template, request, url_for, Blueprint
from project.models import Owner

owners_blueprint = Blueprint(
    'owners',
    __name__,
    template_folder='templates'
)

@owners_blueprint.route('/', methods =["GET", "POST"])
def index():
    return render_template('index.html', owners=Owner.query.all())
~~~~

Now let's build a simple index page, just like we have seen before.

~~~~
{% extends 'base.html' %}

{% block content %}

{% for owner in owners %}
    <p>
        {{owner.first_name}} {{owner.last_name}}
        <br>
    </p>
{% endfor %}

{% endblock %}
~~~~

We should now be able to see all of our owners at [localhost:5000/owners](localhost:5000/owners). So let's make some new ones!

### New + Create

Before we create, we need a route, template and form for creating a new owner. Let's start with the form. In our `projects/owners/forms.py` let's add a new form using FlaskWTF.

~~~~
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class OwnerForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    pass
~~~~

Now let's add a route that renders it!

~~~~
# make sure to import it!
from project.owners.forms import OwnerForm

@owners_blueprint.route('/new')
def new():
    form = OwnerForm()
    return render_template('new.html', form=form)
~~~~

And finally a view for a new owner inside of `project/owners/templates/new.html`:

~~~~
{% extends 'base.html' %}

{% block content %}

<form method="POST" action="{{url_for('owners.index')}}">
    {{ form.csrf_token }}
  <p>
    {{ form.first_name(placeholder="First Name") }}
    <span>
      {% if form.first_name.errors %}
        {% for error in form.first_name.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <p>
  <p>
    {{ form.last_name(placeholder="Last Name") }}
    <span>
      {% if form.last_name.errors %}
        {% for error in form.last_name.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <button type="submit">Add Owner!</button>
</form>

{% endblock %}
~~~~

With your server running, try to access this route. You should get this error: `KeyError: 'A secret key is required to use CSRF.'` Whoops - we forgot to set our secret key! Be sure to do that in the `project` folder's `__init__.py`. (If you don't remember how to set this, go back and review the previous chapter.)

Now let's add a route for when we create a new owner!

~~~~
# make sure to import the db for saving!
from project import db

# here is what our route should look like with GET and POST
@owners_blueprint.route('/', methods =["GET", "POST"])
def index():
    if request.method == "POST":
        form = OwnerForm(request.form)
        if form.validate():
            new_owner = Owner(request.form['first_name'], request.form['last_name'])
            db.session.add(new_owner)
            db.session.commit()
            return redirect(url_for('owners.index'))
        return render_template('new.html', form=form)
    return render_template('index.html', owners=Owner.query.all())
~~~~

### Edit

To edit, we need to find our record first and then send the form:

~~~~
@owners_blueprint.route('/<int:id>/edit')
def edit(id):
    owner=Owner.query.get(id)
    form = OwnerForm(obj=owner)
    return render_template('edit.html', form=form, owner=owner)
~~~~

Now we need a form to edit:

~~~~
{% extends 'base.html' %}

{% block content %}

<form method="POST" action="{{url_for('owners.show', id=owner.id)}}?_method=PATCH">
  {{ form.csrf_token }}
  <p>
    {{ form.first_name(placeholder="First Name") }}
    <span>
      {% if form.first_name.errors %}
        {% for error in form.first_name.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <p>
    {{ form.last_name(placeholder="Last Name") }}
    <span>
      {% if form.last_name.errors %}
        {% for error in form.last_name.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <button type="submit">Edit Owner!</button>
</form>

{% endblock %}
~~~~

Since our show, delete, and update routes are all the same, let's create them at once!

### Show, Delete, Update

~~~~
{% extends 'base.html' %}
{% block content %}
    <h1>Welcome to the show page!</h1>
    <p>Delete me?</p>

    <form method="POST" action="{{url_for('owners.show', id=owner.id)}}?_method=DELETE">
        <input type="submit" value="X">
    </form>
{% endblock %}
~~~~

~~~~
@owners_blueprint.route('/<int:id>', methods =["GET", "PATCH", "DELETE"])
def show(id):
    found_owner = Owner.query.get(id)
    if request.method == b"PATCH":
        form = OwnerForm(request.form)
        if form.validate():
            found_owner.first_name = request.form['first_name']
            found_owner.last_name = request.form['last_name']
            db.session.add(found_owner)
            db.session.commit()
            return redirect(url_for('owners.index'))
        return render_template('edit.html', form=form, owner=found_owner)
    if request.method == b"DELETE":
        form = DeleteForm(request.form)
        if form.validate():
            db.session.delete(found_owner)
            db.session.commit()
        return redirect(url_for('owners.index'))
    return render_template('show.html', owner=found_owner)
~~~~

Now all that's left is to add delete buttons to our application. You can place these wherever makes the most sense to you: on the `index`, `show`, or `edit` pages. Here's how a modified `index` page might look:

~~~~
{% extends 'base.html' %}

{% block content %}

{% for owner in owners %}
  <p>{{owner.first_name}} {{owner.last_name}}</p>
  <form action="{{ url_for('owners.show', id=owner.id) }}?_method=DELETE" method="POST">
    <button type="submit">Delete this owner!</button>
  </form>
{% endfor %}

{% endblock %}
~~~~

Congratulations! We've got a working CRUD app using blueprints. You can read much more about blueprints [here](http://flask.pocoo.org/docs/latest/blueprints/). If you notice above, we did not add CSRF validation when deleting an owner - make sure you add this on your own!

### Screencast

If you'd like to see an example of adding Blueprints to a Flask application, feel free to watch the screencast below.

Screencast: https://vimeo.com/244962661

### Exercise

Complete the [blueprints exercise](https://github.com/rithmschool/python_curriculum_exercises/blob/master/Unit-02/01-blueprints/readme.md).

When you're ready, move on to [Many to Many and Complex Associations](/courses/intermediate-flask/many-to-many-and-complex-associations)