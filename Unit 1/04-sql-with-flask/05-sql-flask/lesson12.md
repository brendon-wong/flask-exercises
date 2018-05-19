### Objectives:

By the end of this chapter, you should be able to:

*   Include the `psycopg2` module to connect to a PostgreSQL database
*   Build a database backed application that performs full CRUD on a resource

### Getting started

In a previous chapter, we built our first CRUD app with Flask on a toy resource. But you may have noticed that our application has a pretty serious flaw: if you stop the server and restart it, you lose any changes you've made to the list of toys! This isn't something we can allow in professional web applications; imagine the outcry if Google lost all of your emails anytime one of its servers went down or needed to be restarted.

To fix this problem, we need our server to communicate with a database which will store our data for us. So let's get started! To begin, we'll make a new virtual environment and install the `psycopg2` module

~~~~
mkvirtualenv flask-sql
pip install flask psycopg2
createdb flask-sql
~~~~

So what's `psycopg2`, you ask? You can think of it as a Python API which allows us to communicate with a database. For help unpacking some of the technical terms, check out [this](http://dba.stackexchange.com/questions/111969/what-exactly-is-psycopg2) StackExchange question.

Let's start by creating a file called `db.py`, which will contain all of our methods for performing CRUD on a database. In our `db.py` let's add the following

~~~~
import psycopg2

def connect():
    c = psycopg2.connect("dbname=flask-sql")
    return c
~~~~

This `connect` function creates a connection. As we'll see below, once you're finished with the connection, you'll need to call the `close` method on it.

Run your `db.py` code from the terminal as follows:

~~~~
python -i db.py
~~~~

The `-i` flag will throw you in to a Python REPL once the code inside of `db.py` executes, so that you'll have access to the `connect` function. Next, try opening a connection!

Once a connection is made, we can open a cursor to perform database operations. This cursor is very similar to the File IO cursor. It's an object used to perform certain operations. We can access our cursor using the `.cursor` method on a connection:

~~~~
conn = connect()
cur = conn.cursor()
~~~~

We can now use the `cur` variable to execute SQL statements. In your Python REPL, try running this commands:

~~~~
# let's create a table:
cur.execute("CREATE TABLE users (id serial PRIMARY KEY, first_name text, last_name text);")

# and a row
cur.execute("INSERT INTO users (first_name, last_name) VALUES (%s, %s)",('Elie', 'Schoppik'))

# Save changes to the database
conn.commit()

# Let's get some data
cur.execute("SELECT * FROM users")
cur.fetchone() # (1, 'Elie', 'Schoppik')

# Close database connection
cur.close()
conn.close()
~~~~

Remember that once the cursor has reached the end, it is done! If you try to fetch the first row twice, you won't be able to. You'll first need to execute the query again.

~~~~
cur.execute("select * from users")
cur.fetchone() # (1, 'Elie', 'Schoppik')
cur.fetchone() # None
~~~~

For a full list of methods available on the cursor object, check the [docs](http://initd.org/psycopg/docs/cursor.html)

### SQL Injection

As we start building larger applications with more technologies, we open ourselves up to more security concerns. One of the most common attacks/hacks that we open ourselves up to when working with SQL is SQL injection.

SQL Injection (SQLi) refers to an injection attack wherein an attacker can execute malicious SQL statements (also commonly referred to as a malicious payload) that control a web application's database server. These malicious attacks include creating records, deleting records and pretty much everything imaginable you can do with a database.

The golden rule of thumb is **Warning Never, never, NEVER use Python string concatenation (+) or string parameters interpolation (%) to pass variables to a SQL query string. Not even at gunpoint.**

You can read more about SQL injection from the docs on psycopg2, [http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries](http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries), [Wikipedia](https://en.wikipedia.org/wiki/SQL_injection), or truly check your understanding with this famous xkcd [comic](http://xkcd.com/327/).

### Refactoring our toy app

Now that you have an idea of how `psycopg2` works, let's try to add more to the `db.py` file and import it into your `app.py` so that we can save a resource permanently!

For now, let's ignore our `Toy` class; we'll come back to using classes soon enough, but since we're writing raw SQL to communicate with our database, it will be easier for now to just deal with strings rather than instances of a `Toy` class.

To begin, let's create a new database from the terminal:

~~~~
createdb flask-toys
~~~~

Next, let's create a toy table. We could do this from `psql`, but for practice let's create the table using `psycopg2`. Open up a Python REPL in the terminal, then do the following:

~~~~
import psycopg2

conn = psycopg2.connect("dbname=flask-toys user=postgres")
cur = conn.cursor()
cur.execute("CREATE TABLE toys (id serial PRIMARY KEY, name text);")

# let's add some starter data
cur.execute("INSERT INTO toys (name) VALUES (%s)", ("duplo",))
cur.execute("INSERT INTO toys (name) VALUES (%s)", ("lego",))
cur.execute("INSERT INTO toys (name) VALUES (%s)", ("knex",))
conn.commit()

# make sure data was saved
cur.execute("SELECT * FROM toys")
cur.fetchall() # should get [(1, 'duplo'), (2, 'lego'), (3, 'knex')]

cur.close()
conn.close()
~~~~

With our database set up and seeded with some starter data, let's now work on refactoring our application to use a database. Let's first add a method to our `db.py` which will grab all of our toys:

~~~~
import psycopg2

def connect():
  c = psycopg2.connect("dbname=flask-toys user=Matt")
  return c

def get_all_toys():
  conn = connect()
  cur = conn.cursor()
  cur.execute("SELECT * FROM toys")
  toys = cur.fetchall()
  cur.close()
  conn.close()
  return toys
~~~~

Next, we need to modify our `app.py`. We can remove references to the `Toy` class and the initialization of a `toys` list, since that data now lives in the database. We'll also need to fix our `index` function so that it makes a call to `get_all_toys()`. Here's what the beginning of your `app.py` should look like:

~~~~
from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
import db

app = Flask(__name__)
modus = Modus(app)

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
         # This isn't right - we'll fix it shortly!
        toys.append(Toy(request.form['name']))
        return redirect(url_for('index'))
    return render_template('index.html', toys=db.get_all_toys())
~~~~

If you start your application and go to `localhost:3000/toys`, however, you'll see a problem: the names of the toys aren't showing up! That's because the `toys` variable now refers to a list of tuples, not a list of `Toy` instances. As we saw before, each tuple in the `toys` list consists of two things: the toy's id (at index 0), and the name (at index 1). So in order to fix our HTMl, we need to replace `toy.name` in our `index.html` with `toy[1]`:

~~~~
{% extends 'base.html' %}
{% block content %}
    <ul>
    {% for toy in toys %}
        <li>{{ toy[1] }}</li>
    {% endfor %}
    </ul>
{% endblock %}
~~~~

Now the toys should show up when you go to `localhost:5000/toys`.

Let's refactor a bit more. Our route to `/toys/new` doesn't need to be changed, since that just renders a form. However, once we submit the form, we need to change the logic that handles our POST request. let's first create a function in our `db.py` file that handles the creation of a new toy:

~~~~
def add_toy(name):
  conn = connect()
  cur = conn.cursor()
  cur.execute("INSERT INTO toys (name) VALUES (%s)", (name,))
  conn.commit()
  cur.close()
  conn.close()
~~~~

We can now finish refactoring our `index` function in `app.py` to completely eliminate any reference to our old `Toy` class:

~~~~
@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.add_toy(request.form['name'])
        return redirect(url_for('index'))
    return render_template('index.html', toys=db.get_all_toys())
~~~~

With this, you should see that adding toys in your web application still works. But now, if you kill the server and start it up again, any new toys you've added will still be there! That's the power of persistence.

### Exercise

Refactor the rest of your `app.py` to use your `flask-toys` database. Try to keep as much of the database logic as possible in your `db.py`. You can try to refactor code in there too; you may already notice a fair amount of code duplication between our `get_all_toys` and our `add_toy` functions.

Next, complete the [SQL with Flask](https://github.com/rithmschool/python_curriculum_exercises/tree/master/Unit-01/05-sql-flask) exercise.

When you're ready, move on to [SQL Alchemy with Flask](/courses/flask-fundamentals/sqlalchemy-with-flask)