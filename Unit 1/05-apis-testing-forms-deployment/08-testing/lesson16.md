### Objectives:

By the end of this chapter, you should be able to:

*   Use `jsonify` to respond with JSON
*   Understand the limitations of `jsonify` with serializing objects

### Using `jsonify` to respond with JSON

So far, all of our Flask applications have used templates to render and return HTML when the user makes a `GET` request. However, it's not always the case that you want your server to respond with HTML. In fact, for many modern architectures (including single page applications), it's often preferable for the server to respond with JSON. Once the data is received, the view can be modified JavaScript.

So how can we build Flask apps that send back JSON instead of HTML? Let's find out! (As always, if you're looking to dig deeper, check out the [docs](http://flask.pocoo.org/docs/0.11/api/).)

The simplest way to respond with JSON is to use Flask's `jsonify` function, which converts Python data types into JSON.

Let's take a look at how `jsonify` works. As always, let's start with a fresh virtual environment:

~~~~
mkvirtualenv flask-json
pip install flask
~~~~

Next, create an `app.py` and put the following code inside of it:

~~~~
from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    person = dict(first='Elie', last='Schoppik', job='Instructor')
    return person
~~~~

If you head to `localhost:5000` you should see an error: `TypeError: 'dict' object is not callable`. What's really happening is that Flask doesn't know how to pass a dictionary, which is a Python-specific data structure, to the client. Let's fix this by converting the data into JSON:

~~~~
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def welcome():
    person = dict(first='Elie', last='Schoppik', job='Instructor')
    return jsonify(person)
~~~~

If we head to `localhost:5000` this time, we should see a JSON representation of our data!

### Serialization of `Flask-SQLAlchemy` objects

So far, so good. But we typically aren't dealing with dictionaries when we build our Flask applications: it's more common for us to use an ORM like `Flask-SQLAlchemy` so that we can create custom objects from some class representing our resource. Let's see what happens if we try to convert that data using `jsonify`.

To begin, set up your `flask-json` application to use Blueprints. Don't worry about template folders or any HTML files, though, as this application will only ever respond with JSON! Try to do this from scratch; if you have trouble, go back to the [blueprints chapter](./01-blueprints.md).

Let's create a blueprint for a single resource, with a model of `Book`. Inside of your `project/books/models.py`, let's create the following class:

~~~~
from project import db

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text)
  author = db.Column(db.Text)

  def __init__(self, title, author):
    self.title = title
    self.author = author
~~~~

Use `flask_migrate` to create the appropriate table in your database. Then hop into `IPython` and create some books.

~~~~
from project.books.models Book
from project import db
book1 = Book("Jurassic Park", "Michael Crichton")
book2 = Book("Don Quixote","Miguel de Cervantes")
db.session.add_all([book1,book2])
db.session.commit()
~~~~

#### GET requests

So far, so good. Now let's set up a route to receive `GET` requests to `/books`. In your `project/books/views.py`, add the following code:

~~~~
from flask import Blueprint, jsonify
from project.books.models import Book

books_blueprint = Blueprint(
  'books',
  __name__
) # no need for a templates folder, as we aren't returning HTML!

@books_blueprint.route('/')
def index():
  return jsonify(Book.query.all())
~~~~

Start up your server and in the terminal type `curl localhost:5000/api/books/` (be sure that your blueprint is registered on `api/books`!). Unfortunately, you should see an error: `TypeError: <__main__.Book object at 0x104659ac8> is not JSON serializable` In other words, Flask doesn't know how to convert, or _serialize_, instances of our `Book` class into JSON.

For now, let's fix this error by manually converting each `Book` instance into a dictionary (we'll get to a better approach soon):

~~~~
from flask import Blueprint, jsonify
from project.books.models import Book

books_blueprint = Blueprint(
  'books',
  __name__
)

@books_blueprint.route('/')
def index():
  return jsonify([
    {'id': book.id, 'author': book.author, 'title': book.title}
    for book in Book.query.all()
  ])
~~~~

#### POST requests

Once you've verified that your `GET /api/books` route is working, let's implement a `POST /api/books` route to create a new book. One important difference to note when we're working with JSON is that the data we send over will live inside of `request.json`, not `request.body` (as it does with form submissions).

Here's one way to implement the `POST` logic:

~~~~
from flask import Blueprint, request, jsonify
from project.books.models import Book
from project import db

books_blueprint = Blueprint(
  'books',
  __name__
)

@books_blueprint.route('/', methods=["GET", "POST"])
def index():
  if request.method == 'POST':
    new_book = Book(
      author=request.json['author'],
      title=request.json['title']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
      'id': new_book.id,
      'author': new_book.author,
      'title': new_book.title
    })
  return jsonify([
    {'id': book.id, 'author': book.author, 'title': book.title}
    for book in Book.query.all()
  ])
~~~~

Once again, in the logic for the `POST` request we're having to manually serialize our book instance so that it can be sent over in the response. Note that a common convention when creating a JSON API is for the `POST` route to return data on the newly created resource.

You can test this route using `curl`. Just be sure to set the right headers!

~~~~
curl localhost:5000/api/books/ -d '{"author": "Serge Lang", "title": "Algebra"}' -H "Content-type: application/json"
# should return data on this new book
~~~~

### Next Steps

As you continue to build more complex schemas, it will become more and more difficult to use `jsonify` to serialize complex data. Later on, we'll learn how to use a module called `flask-restful` to build more complex APIs and serialize with ease!

When you're ready, move on to [Testing with Flask](/courses/flask-fundamentals/testing-with-flask)