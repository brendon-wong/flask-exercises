## Authentication with Flask Login

### Objectives:

By the end of this chapter, you should be able to:

*   Include `flask_login` to refactor authentication logic
*   Implement authentication using `flask_login`
*   Understand what additions must be made to the `User` class for `flask_login` to work

### `flask_login` setup

So far we have seen how to write our own authentication, but it took quite a bit of code and we still had a couple more methods we would have liked to implement. Thankfully, there is a very commonly used module called `flask_login`, which we can use to handle authentication for us! Let's get started by creating a virtual environment.

~~~~
mkvirtualenv flask_login
createdb flask_login
pip install flask flask-sqlalchemy psycopg2 flask-migrate flask-login flask-modus ipython
~~~~

The most important parts of setting up a `flask-login` application are the following, which should go inside of `project/__init__.py`:

~~~~
from flask_login import LoginManager

# initialize the login_manager
login_manager = LoginManager()

# pass your app into the login_manager instance
login_manager.init_app(app)

# You also need to tell flask_login where it should redirect 
# someone to if they try to access a private route.
login_manager.login_view = "users.login"

# You can also change the default message when someone 
# gets redirected to the login page. The default message is
# "Please log in to access this page."
login_manager.login_message = "Please log in!"

# write a method with the user_loader decorator so that flask_login can find a current_user 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
~~~~

We also **must** properly define our `User` model.

### The User Class

For `flask_login` to work, the class that you use to represent users (our User class) **must** implement these properties and methods:

`is_authenticated` - As the name suggests, this checks whether a user is authenticated. In other words, it validates the user's credentials.

`is_active` - What "active" means can vary from application to application, but in general it means more than simply being authenticated. For instance, it may mean that the user has taken a step to activate his or her account, or that the account is not suspended. If you have some custom rules governing the rejection of an account, `is_active` can check for these too.

`is_anonymous` - This checks whether a user is anonymous; if yes, it should return `True`, and if not, it should return `False`.

`get_id()` - This method returns a unique identifier for the user, which can be used to grab the user from `user_loader`. **Note** this method must return a unicode; you'll need to explicitly convert the id to unicode if your ids are some other data type by default.

To make implementing a user class easier, you can inherit from `UserMixin`, which provides default implementations for all of these properties and methods. **We will be using this option instead of writing the methods on our own**

Here is what the user model now looks like with a UserMixin from flask_login

~~~~
from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
~~~~

### Additional Helper Functions and Utilities

`login_user(user_obj)` - this function does the act of "logging in" the user and sets necessary information in the session (just like we did in the last chapter).

`logout_user()` - this function does the act of "logging out" the user and removes information from the session (just like we did in the last chapter).

`current_user` - accessible in our views as well as controllers. This object represents the user that is logged in (just like the one we made in the last chapter).

`@login_required` - this decorator is placed after our route decorator and ensures that the user is logged in or it redirects them to whatever value you have set for `login_manager.login_view`. Very commonly this will be `login_manager.login_view = "users.login"`, but make sure you have this or you will get a `401` error. You can also customize the login message that is flashed to users using `login_manager.login_message`

`user_obj.is_authenticated` - this attribute on the user class returns True or False if a user is logged in. This is very helpful in our `views` for conditional rendering logic.

### Refactoring our Previous app

To see how we can use these methods and values provided by `Flask-Login`, take a look at the [sample](./examples/flask_login) app from the previous chapter, which has been refactored to use Flask Login. You can see configuration changes in the `__init__.py`, as well as refactors to the `users.views` file.

### Adding remember_me cookies

Very commonly when a user logs into a site, there is a check box for remembering their information. “Remember Me” functionality can be tricky to implement. However, Flask-Login makes it nearly transparent - just pass `remember=True` to the `login_user` call. A cookie will be saved on the user’s computer, and then Flask-Login will automatically restore the user ID from that cookie if it is not in the session. The cookie is tamper-proof, so if the user tampers with it (i.e. inserts someone else’s user ID in place of their own), the cookie will merely be rejected, as if it was not there. You can read more about it [here](https://flask-login.readthedocs.io/en/latest/#remember-me).

### Screencast

If you'd like to see an example of adding Flask-Login to a Flask application, feel free to watch the screencast below.

Screencast: https://vimeo.com/244952268

### Testing authentication

Testing authentication with `flask_login` is very nice as we can import helpers like `current_user` and make use of `current_user.is_authenticated`. Here are what some tests might look like - make sure you add your own to the assignment!

~~~~
import unittest 

class TestUser(unittest.BaseTestCase):
    def setUp(self):
    """Disable CSRF, initialize a sqlite DB and seed a user"""
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        db.create_all()
        user = User("eschoppik", "secret")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """drop the db after each test"""
        db.drop_all()

    def test_user_registeration(self):
    """Ensure user can register"""
        with self.client:
            response = self.client.post('/signup', data=dict(
                username='tigarcia',password='moxie'
            ), follow_redirects=True)
            self.assertIn(b'You are logged in!', response.data)
            self.assertTrue(current_user.username == "tigarcia")
            # make sure we hash the password!
            self.assertNotEqual(current_user.password, "moxie")
            self.assertTrue(current_user.is_authenticated)

    def test_incorrect_user_registeration(self):
    """# Errors are thrown during an incorrect user registration"""
        with self.client:
            response = self.client.post('/signup', data=dict(
                username='eschoppik',password='doesnotmatter'))
            self.assertIn(b'Username already exists', response.data)
            self.assertIn('/signup', request.url)

    def test_get_by_id(self):
    """Ensure id is correct for the current/logged in user"""
        with self.client:
            self.client.post('/login', data=dict(
                username="admin", password='admin'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    def test_check_password(self):
    """ Ensure given password is correct after unhashing """
        user = User.query.filter_by(username='admin').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'notadmin'))

    def test_login_page_loads(self):
    """Ensure that the login page loads correctly"""
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    def test_correct_login(self):
    """User should be authenticated upon successful login and stored in current user"""
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="eschoppik", password="secret"),
                follow_redirects=True
            )
            self.assertIn(b'Logged in!', response.data)
            self.assertTrue(current_user.username == "eschoppik")
            self.assertTrue(current_user.is_authenticated)

    def test_incorrect_login(self):
    """The correct flash message is sent when incorrect info is posted"""
        response = self.client.post(
            '/login',
            data=dict(username="dsadsa", password="dsadsadsa"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials', response.data)

    def test_logout(self):
    """Make sure log out actually logs out a user"""
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="eschoppik", password="secret"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You are logged out!', response.data)
            self.assertFalse(current_user.is_authenticated)

    def test_logout_route_requires_login(self):
    """Make sure that you can not log out without being logged in"""
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)
~~~~

When you're ready, move on to [OAuth with Flask](/courses/intermediate-flask/oauth-with-flask)