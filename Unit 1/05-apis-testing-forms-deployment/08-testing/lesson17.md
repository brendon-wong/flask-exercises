## Testing with Flask

### Objectives:

By the end of this chapter, you should be able to:

*   Understand the drawbacks of using a doctest
*   Include unittest and write simple assertions with life cycle methods
*   Test render and redirects with Flask

### Writing a doctest or using assert

One of the simplest ways of writing a test is to actually use a docstring! To describe our tests we can write a docstring and run `python3 -m doctest name_of_file.py`. Let's look at a small example; create a file called `testing.py` and put this string in the file:

~~~~
"""
  adding two numbers together

  >>> 2 + 2
  4

  multiplying two numbers together

  >>> 3 * 2
  5
"""
~~~~

If you run `python3 -m doctest testing.py`, you should see information about the failing test. (If you run `python3 -m doctest -v testing.py`, you'll see information on all tests, not just the failing one.)

While doctests may look interesting, they are not particularly useful when working with larger files, as they can be difficult to structure. Thankfully, there is another way we can quickly make assertions about our code: using the `assert` command! We can assert some expression and if it evaluates to `True` we will continue and if it evaluates to anything else, it will raise an `Assertion Error`

~~~~
assert 1 == 1
l1 = [1,2,3]
l2 = [1,2,3]

assert l1 == l2

l1.append(5)

assert l1 == l2 # AssertionError
~~~~

While this is pretty neat, it's not the easiest to work with at a larger scale, so we need something a bit more powerful so that we can test our code outside of the actual file our code is in. Thankfully, Python comes with a module called `unittest`, which is great for testing and assertions!

### Testing with unittest

Let's start by importing the `unittest` module and create a class that inherits from `unittest.TestCase`.

Inside of each instance method (which we _have_ to start with `test`), we can use methods on `self` to make assertions. To run our tests we use the `unittest.main()` method. Let's make a file called `test.py` and try it out!

~~~~
import unittest

def addition(num1, num2):
    if (num1 < 0):
        num1 *= -1
    if (num2 < 0):
        num2 *= -1

    return num1 + num2

class AppTests(unittest.TestCase):

    def test_addition(self):
        # assert addition(5,5) == 10
        self.assertEqual(addition(5,5),10)

    def test_addition_not_equal(self):
        # assert not addition(5,5) == 0
        self.assertNotEqual(addition(5,5),0)

    def test_numbers(self):
        self.assertLess(5, 10)
        self.assertLessEqual(5, 5)
        self.assertGreater(10,5)
        self.assertGreaterEqual(10,10)
        self.assertGreaterEqual(10,9)

if __name__ == '__main__':
    unittest.main()
    # All tests have to start with the word tests!
~~~~

When we run this file using `python3 test.py` we should see something like this:

~~~~
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
~~~~

Now let's see what it looks like when a test fails. Change your file to included `test_adding_negatives`:

~~~~
import unittest

def addition(num1, num2):
    if (num1 < 0):
        num1 *= -1
    if (num2 < 0):
        num2 *= -1

    return num1 + num2

class AppTests(unittest.TestCase):

    def test_addition(self):
        # assert addition(5,5) == 10
        self.assertEqual(addition(5,5),10)

    def test_addition_not_equal(self):
        # assert not addition(5,5) == 0
        self.assertNotEqual(addition(5,5),0)

    def test_adding_negatives(self):
        self.assertEqual(addition(-1, -2), -3)

    def test_numbers(self):
        self.assertLess(5, 10)
        self.assertLessEqual(5, 5)
        self.assertGreater(10,5)
        self.assertGreaterEqual(10,10)
        self.assertGreaterEqual(10,9)

if __name__ == '__main__':
    unittest.main()
    # All tests have to start with the word tests!
~~~~

Now your output should look like this:

~~~~
F...
======================================================================
FAIL: test_adding_negatives (__main__.AppTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test.py", line 23, in test_adding_negatives
    self.assertEqual(addition(-1, -2), -3)
AssertionError: 3 != -3

----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=1)
~~~~

Notice in the output the line `F...`. Each dot stands for a passing test and each `F` stands for a failing test. So we can see quickly that 1 test failed and 3 passed.

Also, the output gives us a starting point to look at for why the test failed. On `line 23`, our assertion failed. We should conclude from the failure that we need to change the addition function somehow.

So, why did the test fail? Well our addition function doesn't do normal addition. It actually adds the absolute value of numbers (makes numbers positive before adding). If we want our implementation to work like normal addition, we would have to change our `addition` function to get the tests passing.

Note that if you change any of the function names so that they don't start with `test_`, the tests inside of the function won't run!

### docstrings

When we run these tests, we are not seeing much information about them in the terminal. This is unlike JavaScript, where we could put in as much text to describe our tests and the expectations as we wanted. So how do we do that in Python? We use docstrings! Let's refactor our previous tests to use docstrings to see the information a bit better.

~~~~
import unittest

def addition(num1, num2):
    return num1 + num2

class AppTests(unittest.TestCase):

    def test_addition_not_equal(self):
        """Lets make sure that addition(5,1) == 6"""
        # assert not addition(5,5) == 0
        self.assertNotEqual(addition(5,5),0)

    def test_adding_negatives(self):
        """Let's make sure that addition of negatives works: addition(-1, -2) == -3"""
        self.assertEqual(addition(-1, -2), -3)

    def test_numbers(self):
        """Basic Less Than/Greater Than Tests With Numbers"""
        self.assertLess(5, 10)
        self.assertLessEqual(5, 5)
        self.assertGreater(10,5)
        self.assertGreaterEqual(10,10)
        self.assertGreaterEqual(10,9)

if __name__ == '__main__':
    unittest.main()
    # All tests have to start with the word tests!
~~~~

Now when we run this, make sure to add the `-v` flag: `python3 test.py -v`

### setUp + tearDown

If we would like code to run before all of our tests, we can add a special method called `setUp` to do that. If we want code to run after each test, we can run `tearDown`.

Here's an example:

~~~~
import unittest

class AppTests(unittest.TestCase):

    def setUp(self):
        # run before every single test
        self.instructor = "Elie"

    def tearDown(self):
        # If we would like code to run after all of our tests,
        # we can add a special method called `tearDown` to do that.
        pass

    def test_set_up(self):
        self.assertTrue(self.instructor == "Elie")

    def test_contains(self):
        self.assertIn(4, [1,2,3,4])

    def test_instance(self):
        self.assertIsInstance([], list)
        self.assertIsInstance(3, int)

    def test_expect_errors(self):
        with self.assertRaises(NameError):
            value_does_not_exist

if __name__ == '__main__':
    unittest.main()
    # All tests have to start with the word tests!
~~~~

### Testing Flask applications

Now that we've seen examples of how to test our code, let's try writing some tests for a simple Flask application. We can use `unittest` alone to write our tests, but there is another useful module called `flask-testing` which will help us test a bit easier. Let's create a virtual environment, then install the necessary packages

~~~~
mkvirtualenv flask-testing
workon flask-testing
pip install flask psycopg2 flask-sqlalchemy flask-testing flask_modus flask_script flask_migrate
createdb flask-testing
~~~~

Next, create an `app.py` file and include the following code:

~~~~
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def welcome():
    return "Hello World!"

@app.route('/back')
def go_back():
    return redirect(url_for('welcome'))
~~~~

### Testing Render and Redirect

Now let's add some tests using `flask_testing` and `unittest`. Put this code into a `test.py`:

~~~~
from app import app
from flask_testing import TestCase
import unittest

class BaseTestCase(TestCase):
    def create_app(self):
        return app

    def test_render(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello World!', response.data)

    def test_redirect(self):
        response = self.client.get(
            '/back', follow_redirects=True
        )
        self.assertIn(b'Hello World', response.data)

if __name__ == '__main__':
    unittest.main()
~~~~

If you run `python test.py -v`, you should see two tests passing. There are a few salient features of the above example that you should pay attention to. First, notice that the class we create inherits from `TestCase`, which comes from `flask_testing`. Inside of our class, we **must** include a `create_app` method which returns a Flask instance (otherwise, you'll get an error).

Other than that, the syntax should like similar to what we've already seen. For a full list of features unique to Flask-testing, check out the [docs](https://pythonhosted.org/Flask-Testing/).

### Testing a Database

We've built our first test-driven Flask application, but the app itself doesn't do a whole lot. As a next step, let's introduce a database so that we can test our CRUD operations! Let's add a model for a `Student` and CRUD routes. _Try to do this on your own first._

All finished? Here is what your `app.py` should look like.

~~~~
from flask import Flask, request, redirect, url_for, render_template
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/flask-testing"
modus = Modus(app)
db = SQLAlchemy(app)
Migrate(app, db)

class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/students', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        new_student = Student(request.form['first_name'], request.form['last_name'])
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', students=Student.query.all())

@app.route('/students/new')
def new():
    return render_template('new.html')

@app.route('/students/<int:id>/edit')
def edit(id):
    return render_template('edit.html', student=Student.query.get(id))

@app.route('/students/<int:id>', methods = ["GET", "PATCH", "DELETE"])
def show(id):
    found_student = Student.query.get(id)
    if request.method == b'PATCH':
        found_student.first_name = request.form['first_name']
        found_student.last_name = request.form['last_name']
        db.session.add(found_student)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == b'DELETE':
        db.session.delete(found_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('show.html', student=found_student)
~~~~

After running your migrations, let's add some tests! Let's replace our `test.py` with the following:

~~~~
from app import app,db, Student
from flask_testing import TestCase
import unittest

class BaseTestCase(TestCase):
    def create_app(self):
        # let's use SQLite3 as it is much faster to test with than a larger postgres DB
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        return app

    def setUp(self):
        db.create_all()
        person1 = Student("Elie", "Schoppik")
        person2 = Student("Tim", "Garcia")
        person3 = Student("Matt", "Lane")
        db.session.add_all([person1, person2, person3])
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_index(self):
        response = self.client.get('/students', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Elie Schoppik', response.data)
        self.assertIn(b'Tim Garcia', response.data)
        self.assertIn(b'Matt Lane', response.data)

    def test_show(self):
        response = self.client.get('/students/1')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            '/students',
            data=dict(first_name="New", last_name="Student"),
            follow_redirects=True
        )
        self.assertIn(b'New Student', response.data)

    def test_edit(self):
        response = self.client.get(
            '/students/1/edit'
        )
        self.assertIn(b'Elie', response.data)
        self.assertIn(b'Schoppik', response.data)

    def test_update(self):
        response = self.client.patch(
            '/students/1',
            data=dict(first_name="updated", last_name="information"),
            follow_redirects=True
        )
        self.assertIn(b'updated information', response.data)
        self.assertNotIn(b'Elie Schoppik', response.data)

    def test_delete(self):
        response = self.client.delete(
            '/students/1',
            follow_redirects=True
        )
        self.assertNotIn(b'Elie Schoppik', response.data)

if __name__ == '__main__':
    unittest.main()
~~~~

If you run the tests now (by typing `python test.py`), unfortunately, you'll see that they all fail. But this is because you haven't written any HTML! In order for these tests to pass, we need to have an `index.html`, `edit.html`, `new.html`, and `show.html`. Create some HTML (or use some from an earlier app). Once the HTML is there, the tests should pass.

### Running Tests

As you grow the number of tests you have it becomes much easier to have tool run tests for you. There are a couple of popular ones with Python, including `nose` and `green`. You can install either of these via `pip` and simply run those commands from the command line. These tools provide a better looking interface for tests and make running multiple tests in multiple folders much easier.

### Exercise

Complete the [Flask Testing](https://github.com/rithmschool/python_curriculum_exercises/blob/master/Unit-01/08-testing/readme.md) exercise.

When you're ready, move on to [Forms with WTForms](/courses/flask-fundamentals/forms-with-wtforms)