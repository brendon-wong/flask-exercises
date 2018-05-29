### Objectives:

By the end of this chapter, you should be able to:

*   Use `flask-restful` to simplify API creation
*   Build an API that performs CRUD on a single resource

### Using `flask-restful`

If you're building an API that conforms to the conventions of RESTful routing, there's a module you can use to help simplify the process, called `flask-restful`. Flask restful allows us to isolate our API logic in a cleaner fashion and makes it easier to add associations with our API. For a simple working example using Flask restful just for the routing (without worrying about a database), check out the [docs](http://flask-restful.readthedocs.io/en/0.3.5/quickstart.html). For now, we'll focus on refactoring our existing `Book` app using `flask-restful`.

First, we'll need to install it:

~~~~
pip install flask-restful
~~~~

Next, we'll need to import the things we need from it. We'll need to use this module in our `project/books/views.py` file, so let's head to the top of that file and modify what we're importing:

~~~~
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from project.books.models import Book
from project import db
~~~~

To create an API out of our blueprint, we'll need to pass our blueprint into the `Api` class. We can rename our `books_blueprint` and do the following:

~~~~
books_api_bp = Blueprint(
  'books_api',
  __name__
)

books_api = Api(books_api_bp)
~~~~

Now that we have an Api, we can start adding resources to it. The syntax here is as follows:

~~~~
@some_api.resource('/path') # use our api as a decorator!
class SomeAPI(Resource): # create a class that inherits from Resource
    def get(self): # methods inside the class should correspond to HTTP verbs
        pass

    def post(self):
        pass
~~~~

In our case, this means we can refactor our previous code to the following:

~~~~
@books_api.resource('/books')
class BooksAPI(Resource):
  def get(self):
    return jsonify([
      {'id': book.id, 'author': book.author, 'title': book.title}
      for book in Book.query.all()
    ])

  def post(self):
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
~~~~

Finally, we'll need to update our `__init__.py` to import our Api blueprint:

~~~~
from project.books.views import books_api_bp

app.register_blueprint(books_api_bp, url_prefix='/api')
~~~~

### `marshal_with`

This code is better, but there's still a fair amount of redundancy in our API methods. For example, all of the methods in our `BookApi` have to manually serialize data and pass it into `jsonify`. Fortunately, Flask Restful also comes with serialization functionality, so that we can more easily convert between objects and JSON data.

Here's how it works: we need to use Flask-Restful's `marshal_with` function to specify how we should _marshal_ our data. (You can think of marshaling and serializing as essentially synonymous. If you'd like to get into the weeds about the distinction, Stack Overflow has [got your back](http://stackoverflow.com/questions/770474/what-is-the-difference-between-serialization-and-marshaling).) To help with the marshaling, we'll also need to import something else from Flask-Restful.

At the top of your `project/books/views.py`, you can include the following:

~~~~
from flask_restful import Api, Resource, fields, marshal_with

book_fields = {
  'id': fields.Integer,
  'title': fields.String,
  'author': fields.String
}
~~~~

You can then marshal your object data using the `book_fields` dictionary, which tells your application how to treat different attributes in your objects. To actually marshal the data, you use the `@marshal_fields` decorator. Here's how the `get` inside of the `BookListApi` can be refactored:

~~~~
@marshal_with(book_fields)
def get(self):
    return Book.query.all()
~~~~

Even though it looks like we're just returning a list of `Book` instances, including the decorator ensures that our objects will eventually be converted properly, so that the server can respond with JSON.

#### Exercises

1.  Refactor the rest of your books app using what you've learned about `flask_restful`.
2.  Build a CRUD app on a single resource that uses AJAX exclusively: no page reloads allowed.

When you're ready, move on to [Authenticating a Flask API with JWTs](/courses/intermediate-flask/flask-jwt-authentication)