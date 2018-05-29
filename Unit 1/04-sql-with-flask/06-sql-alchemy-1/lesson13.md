## SQL Alchemy with Flask

### Objectives:

By the end of this chapter, you should be able to:

*   Explain what an ORM is
*   Describe the benefits and drawbacks of using an ORM
*   Include SQLAlchemy to perform full CRUD on a resource

In the last chapter, we refactored our toy app to use a database. However, in the process we also lost something: your HTML files are a little less readable than they were when you were using a `Toy` class to create toys. For example, prior to adding a database, our `index.html` looked like this:

~~~~
{% extends 'base.html' %}
{% block content %}
    <ul>
    {% for toy in toys %}
        <li>{{ toy.name }}</li>
    {% endfor %}
    </ul>
{% endblock %}
~~~~

However, since `psycopg2` returns lists of tuples to us, not instances of a `Toy` class, we had to rewrite our `index.html` as follows:

~~~~
{% extends 'base.html' %}
{% block content %}
    <ul>
    {% for toy in toys %}
        <li>{{ toy\[1\] }}</li>
    {% endfor %}
    </ul>
{% endblock %}
~~~~

In particular, we had to replace `toy.name`, which is a simple and clear description of what will show up on the page, with `toy[1]`, which is more abstract. In this simple application the distinction might not matter much, but imagine if you had a resource with dozens of attributes rather than just a single one! Trying to keep track of which index in a tuple corresponded to which attribute you're interested in could quickly become a headache.

So using classes and instances to represent our resources certainly has its benefits. And you could absolutely write some code that takes the tuples you get out of the database and converts them into instances of some class (and vice versa). But thankfully, such tools already exist. They are called ORMs.

### Definitions

**ORM** \- ORM stands for **O**bject **R**elational **M**apping. As the acronym implies, ORMs provide a mapping between objects (in a programming language like Python) to rows in a relational database table.

**Model** \- When using an ORM, you map tables to classes, which in this context we call Models. Each model will have built in class and instance methods for performing CRUD operations.

**SQLAlchemy** SQLAlchemy is an ORM for Python!

We'll be using SQLAlchemy via a tool called Flask-SQLAlchemy, which integrates the two tools. Let's get started and build a new app using this ORM.

### Getting Started

Let's build a CRUD app on computers. As usual, we'll first create a virtual environment:

~~~~
mkvirtualenv flask-sql-alchemy
workon flask-sql-alchemy
pip install flask psycopg2 flask-sqlalchemy flask-modus ipython
createdb computers-db
~~~~

Now let's make an `app.py` and import `flask_sqlalchemy` and create an instance of the `SQLAlchemy` class. We also will need to configure the `DATABASE_URI`, which is how postgres will connect to our flask application.

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(\_\_name\_\_)
app.config\['SQLALCHEMY\_DATABASE\_URI'\] = 'postgres://localhost/computers-db'
app.config\['SQLALCHEMY\_TRACK\_MODIFICATIONS'\] = False
db = SQLAlchemy(app)
~~~~

### Adding a Model

Now if we run `app.py` nothing special is going to happen so let's add a model inside the file. This model will be for our computers resource:

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(\_\_name\_\_)
app.config\['SQLALCHEMY\_DATABASE\_URI'\] = 'postgres://localhost/computers-db'
app.config\['SQLALCHEMY\_TRACK\_MODIFICATIONS'\] = False
db = SQLAlchemy(app)

\# notice that all models inherit from SQLAlchemy's db.Model
class Computer(db.Model):

    \_\_tablename\_\_ = "computers" \# table name will default to name of the model

    \# Create the three columns for our table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    memory\_in\_gb = db.Column(db.Integer)

    \# define what each instance or row in the DB will have (id is taken care of for you)
    def \_\_init\_\_(self, name, memory\_in\_gb):
        self.name = name
        self.memory\_in\_gb = memory\_in\_gb

    \# this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def \_\_repr\_\_(self):
        return f"This {self.name} has {self.memory\_in\_gb} GB of memory"
~~~~

Let's now explore the ORM and seed our database with some data. To do that, open up `ipython` and type the following:

~~~~
from app import db, Computer

\# create the tables in our database....there is a better way to do this we will see soon!
db.create_all()

\# create two instances of our class
my_mac = Computer('Macbook Pro', 8)
my_acer = Computer('Aspire V15', 16)

my_mac.name \# Macbook Pro
my\_mac.memory\_in_gb \# 8
my_mac.id \# None

\# Whoa, what happened to our id? We don't have one yet because we have not saved it!

\# first we need to add our instances individually (or use the add_all method which accepts a list)
db.session.add(my_mac)
db.session.add(my_acer)

\# save it in the database
db.session.commit()

my_mac.id \# 1
my_acer.id \# 2
~~~~

Now that we have some sample records, we can head over to `psql` and connect to the `computers-db` database and if we run `SELECT * FROM computers;` we should see our two computers!

### CRUD With SQLAlchemy

Now let's see what the other CRUD operations look like with SQLAlchemy. Try running these in `ipython` to make sure you're comfortable with them.

#### Create

~~~~
super_computer = Computer('Supercomputer', 128)
db.session.add(super_computer)
db.session.commit()
~~~~

#### Read

To retrieve information from the database we can use the `.all` method to get everything, or the `get` method to just get a specific object by id. If you want to search by something other than id, you can also use the `filter_by` method:

~~~~
all_computers = Computer.query.all() \# returns a list
first_computer = Computer.query.get(1) \# returns a single object with an id of 1
first\_computer = Computer.query.filter\_by(name="Macbook Pro") \# returns a list
first\_computer = Computer.query.filter\_by(name="Macbook Pro").first() \# returns an object
~~~~

#### Update

Flask-SQLAlchemy does not have a built in `update` function, so in order to update, we need to find our data, modify it, and then save it again:

~~~~
first_computer = Computer.query.get(1)
first_computer.model = "Commodore 64"
db.session.add(first_computer)
db.session.commit()
~~~~

#### Delete

To remove something with Flask-SQLAlchemy you first have to find it:

~~~~
found_computer = Computer.query.get(1)
db.session.delete(found_computer)
db.session.commit()
~~~~

### Screencast

If you'd like to see an example of building a CRUD application with Flask-SQLAlchemy, feel free to watch the screencast below.

Screencast: https://www.youtube.com/watch?v=e3S9yYKV97E

### Additional Resources

[http://flask-sqlalchemy.pocoo.org/2.1/](http://flask-sqlalchemy.pocoo.org/2.1/)

### Exercise

Complete the [First Flask-SQLAlchemy](https://github.com/rithmschool/python_curriculum_exercises/tree/master/Unit-01/06-sql-alchemy-1) exercise.

When you're ready, move on to [Migrations with Flask Migrate](/courses/flask-fundamentals/migrations-with-flask-migrate)