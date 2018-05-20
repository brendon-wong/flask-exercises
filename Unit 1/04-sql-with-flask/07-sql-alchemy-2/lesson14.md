### Objectives:

By the end of this chapter, you should be able to:

*   Define what migrations are and why they are useful
*   Use Flask Migrate to generate and run migrations

### Migrations with Flask Migrate

So far we have seen how to create tables using `db.create_all` in Flask-SQLAlchemy. While this might be a viable solution when we work on our own, it is not a maintainable solution when working with others. It would be really nice if we had a system very similar to `git` for changes to our database schema. This is exactly the concept of migrations.

When we write `DDL` (CRUD on tables and columns), we want to make sure everyone is aware of changes to the structure of our data, and that those changes are made on a permanent basis. If your `users` table looks entirely different from your coworker's, it's going to be very difficult for the two of you to make meaningful progress together. Migrations are files that, when run, execute SQL to perform `DDL` on a schema. If you perform an incorrect migration, you can _rollback_, or undo, that change. You can think of using migrations as an analogue to using Git for the entire project. The difference is that migrations are a form of version control specifically for the structure of your data over time.

To use migrations with Flask, we will use the `flask-migrate` package.

Let's start with a virtual environment:

~~~~
mkvirtualenv learn-flask-migrate
workon learn-flask-migrate
pip install flask psycopg2 flask_sqlalchemy flask-migrate ipython
createdb learn-flask-migrate
touch app.py
~~~~

And make a simple `app.py` with a model for a Student.

~~~~
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # importing our latest dependency

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-flask-migrate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db) # this exposes some new flask terminal commands to us!

class Student(db.Model):

    __tablename__ = "students" # table name will default to name of the model

    # Create the three columns for our table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    # define what each instance or row in the DB will have (id is taken care of for you)
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return f"The student's name is {self.first_name} {self.last_name}"
~~~~

Note that our boilerplate up top has some enhancements. First, we're importing a class called `Migrate` from `flask_migrate`. Later on, we're passing this class our `app` along with our `db` instance. Basically, what this does is expose a bunch of new `flask` terminal commands to us. To get started, head into the terminal and type `flask db`. All of your new terminal commands should show up!

### Three Migration Commands

When you're using Flask-Migrate, there are many different commands you'll have access to. In practice, however, there are only three you'll be using frequently. Let's discuss each of them briefly.

#### `init`

To first set up your migrations directory, we can run `flask db init`. This creates a new migration repository; in so doing, this command creates a couple of folders and files in our project root where our migrations will live. We only need to do this **once**. This is analogous to initializing a Git repository: you only need to `git init` a project once.

#### `migrate`

Now that we have our folder structure set up, let's run `flask db migrate`. This will create **pending** migrations for us based on how our **Model** looks. This command essentially creates a python file inside of `/migrations/versions`, which, when executed, will run SQL to make a change to our schema based on the `Model`.

By default, the name of the file that will be created will simply be the uniquely generated ID of the migration. If you'd like to add some human-readable information to the file name, you can do this by adding a message to the migration with the `-m` flag. For example, if you run

~~~~
flask db migrate -m "create student table"
~~~~

You should wind up with a filename that looks something like `ca5cd22ac516_creating_student_table.py` inside of `/migrations/versions`.

It's important to note that this command doesn't actually run the migrations or update the database based on your model. It just creates a file that can be used to update the database. This means you can make changes to the generated file after running this command, and before running the `upgrade` command.

However, there is one way in which this command interacts with the database: if you hop into `psql`, you'll notice that there's now a single table in the database, with a name of `alembic_versions`. This table is used to keep track of the order of the database revision history.

#### `upgrade`

To **run** our **pending** migrations, and make a change to our schema, you can run `flask db upgrade`. If we look in `psql learn-flask-migrate` and type `\dt` we should see our table! If we type `SELECT * FROM students` we should see all of columns as well!

If you look at the file that was created when you issued the `migrate` command, you'll see that there are two functions defined there: `upgrade` and `downgrade`. The `upgrade` function specifies what should happen to the database when you run the `upgrade` command from the terminal. Similarly, the `downgrade` command specifies what happens when you run the `downgrade` command from the terminal. You can think of these commands as being inverse operations. `upgrade` moves you forward in the migration history, `downgrade` moves you backwards. Whatever the `upgrade` command in a migration file does, the `downgrade` command should do the opposite. This allows you to move backwards and forwards in the migration history as needed.

Note also that when you run this migration, a row gets added to the `alembic_version` table in your database with the id of the migration.

### Working with Migrations

When you're using migrations to keep track of the database schema over time, you should _never_ be issuing DDL commands to the database directly. Every change to the structure of the database should be recorded in a migration. If you fail to do this you can run into serious problems when collaborating with people who are using the migration files as the single source of truth for the history of the database.

The easiest way to see the problem is with an example. Let's say that you decide your student model doesn't need to record last name anymore. The proper way to get this change recorded is the following:

1.  Delete references to `last_name` in your model,
2.  Run a migration,
3.  Upgrade your database based on the migration.

Suppose that you ignore the migrations though, and instead you hop into psql and drop the column directly:

~~~~
ALTER TABLE students DROP last_name;
~~~~

As expected, this will drop the `last_name` column from the `students` table.

Later on, suppose you decide you want to keep track of students' ages as well as their names. You've forgotten that you dropped the `last_name` column in the database, so you just update the model to account for age:

~~~~
class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
~~~~

If you migrate, everything goes through as expected, but in the terminal output you should see the following lines:

~~~~
INFO  [alembic.autogenerate.compare] Detected added column 'students.age'
INFO  [alembic.autogenerate.compare] Detected added column 'students.last_name'
~~~~

The migration file is adding columns for `last_name` and `age`, since there was a disconnect between the model and the database: the database no longer had `last_name`, but the model did!

For you, there's no problem. You can run the migration by upgrading and everything looks good.

Here's the problem, though. Suppose you've got a colleague who's also working on this project, and who has upgraded to the first migration, but not the second. When she pulls your changes and tries to upgrade based on your latest migration, she'll get an error!

~~~~
sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) column "last_name" of relation "students" already exists
~~~~

The problem is that both migration files add a `last_name` column inside of the `upgrade` function. But you can't add a column where one already exists, and psycopg2 will throw an error. You can duplicate this error for yourself if you downgrade twice, and then try to upgrade.

The moral here: if you're using migrations to keep track of your database schema over time, use migrations _exclusively_. Collaboration quickly becomes a nightmare if people are making changes to the structure of data that isn't reflected in a migration file.

### Screencast

If you'd like to see an example of adding Flask-Migrate to a Flask application, feel free to watch the screencast below.

Screencast: https://www.youtube.com/watch?v=_aDEn4n32uY

When you're ready, move on to [One To Many Associations](/courses/flask-fundamentals/one-to-many-associations)