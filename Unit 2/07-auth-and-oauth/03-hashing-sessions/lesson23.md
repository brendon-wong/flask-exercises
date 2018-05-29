### Objectives:

By the end of this chapter, you should be able to:

*   Compare and contrast cookies and sessions
*   Implement authentication using `session` and `bcrypt`

### Introduction

In the previous section, we learned how to hash a user's password using Bcrypt. This is a great start - you can now build applications that securely store login information for users!

Unfortunately, there is a fatal flaw in our app. If you start the application we worked on, a user can simply navigate to `/welcome` and our app will them that they are logged in! We need some way of protecting this `/welcome` route to make sure that only authenticated users can access the route.

To do this, we need a way to remember information from previous requests and responses. Since the web is stateless, we need some form of storage to remember if a user is logged in. We could use a database, but that would be overkill as we would have to make a table with rows for each time a user logs in. Instead, it would be great if we could store some information in memory on the server. That is exactly what the `session` allows us to do. Flask provides access to a `session` object which is available and persists while our server is running.

### Sessions

Sessions are not an idea unique to Flask. However, if you're curious about how specifically Flask implements sessions, check out [this](https://www.reddit.com/r/flask/comments/5l2gmf/af_eli5_how_sessions_work_in_flask/) thread on Reddit.

You can think of a session as a small collection of data that is stored on the server. The browser is only responsible for storing a session id, which it can pass along in a request so that the server can retrieve data stored in the session. Typically the session data is encrypted with the help of a secret key stored on the server, for additional security.

While Flask comes built-in with a thing called `session`, it's important to understand that the implementation is a bit different than a typical session, in that Flask's sessions are actually **cookie based**. This means that when you use `session` to store data, that data will be signed with a secret key, but also sent back to the browser in a cookie. Anybody can read the data in this cookie, but the server will know if the data has been tampered with. But because the data can be read by the browser, you should **never** store data that needs to be kept secret in with Flask's built-in `session`!

Let's look at a quick example. First, start a new project:

~~~~
mkdir sessions-example
cd sessions-example
mkvirtualenv sessions-example
pip install flask
touch app.py
~~~~

In your `app.py`, include the following:

~~~~
from flask import Flask, session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'

@app.route('/start_counter')
def start_counter():
    session['count'] = 0
    return 'New counter started!'

@app.route('/count')
def count():
    count = session.get('count')
    if isinstance(count, int):
        session['count'] += 1
        return str(session['count'])
    return 'No counter set!'

@app.route('/get_count')
def get_count():
    return str(session.get('count', 'No counter set!'))

@app.route('/clear_count')
def clear_count():
    session.pop('count', None)
    return 'Counter cleared!'

if __name__ == '__main__':
    app.run(debug=True)
~~~~

Now, start the server: `python app.py`.

This small application uses the session to keep track of a running counter across different requests. To start the counter, you can go to `/start_counter`, and to increment the counter you can go to `/count`. You should see that if you make multiple requests to `/count`, the counter on the page increases. This is because the value of the counter is being stored via `session`!

So how exactly is this working? If you're in Chrome, you can head to the Network tab and examine the response. You should see that among the response headers, there's one called `Set-Cookie`, whose value is `session=SOME_STRING`.

![Flask sessions network tab](https://www.rithmschool.com/content/intermediate_flask/flask-session-network-tab.png)

The string to the right of `session` may look like it's encrypted, but it's actually not. In fact, the part of the string to the left of the first dot is just [base64 encoded](https://developer.mozilla.org/en-US/docs/Web/API/WindowBase64/Base64_encoding_and_decoding), and can be decoded with a single line of JavaScript:

~~~~
atob("eyJjb3VudCI6MX0"); // "{"count":1}"
~~~~

Here are a couple of things you should verify:

1.  If you stop the server and restart it, the session persists. But if you quit the browser and restart it, the session is destroyed. In other words, if you have a counter with some positive value, restart the browser, and then refresh the counter, you'll be told that no counter is set.
    
2.  If you try to tamper with the cookie, the session should break. In Chrome, you can try this out in the application tab. Go to the "Cookies" section under "Storage", and then tamper with the value for the session cookie. If you have a counter going, manipulate the cookie, and then refresh the page, you should see that the counter is reset. This is because the server uses the secret key to verify that the cookie has not been tampered with!

![Flask sessions application tab](https://www.rithmschool.com/content/intermediate_flask/flask-session-application-tab.png)

### Remembering that a user has logged in using `session`

When a user successfully logs in, we will add some information in the session (just the user ID) and then for certain routes, we will make sure that the user ID exists in the session; if it doesn't, we will not allow them to access that route.

To help with the UI, we'll also make use of flash messages to help inform the user of what's going on. Right now, the UI can be a little confusing: when things fail, you don't always know why, and when things succeed there could be more clarity around the fact that they've succeeded.

The first thing we'll do is import `session` from Flask, and, when a user is authenticated, place the user's id in the session. This means that the first line of `project/users/views.py` should look like this:

~~~~
from flask import redirect, render_template, request, url_for, Blueprint, session
~~~~

And the new `login` route should look like this. This time, we're storing the result of `User.authenticate` in a variable, since if the user is authenticated we'll want to store their id in the session.

~~~~
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.authenticate(form.data['username'], form.data['password'])
        if user:
            session['user_id'] = user.id
            return redirect(url_for('users.welcome'))
    return render_template('login.html', form=form)
~~~~

### Adding flash messages

Very commonly we want to let our users know that something has happened on the server, like making sure they have logged in successfully. We might think that we can just add that on a page when doing a render, and we would be correct. But what happens when we redirect? We need some way of a value persisting for more than 1 request (since redirects are two requests). To do that, we use something called a _flash message_. A flash message is a piece of information that lives in the session for more than one request and is removed once displayed.

Thankfully we do not have to implement this ourselves. Flask has our back once again! Let's import `flash` from Flask as well, and add a few different flash messages to our application:

~~~~
from flask import redirect, render_template, request, url_for, Blueprint, session, flash
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
            flash("Invalid submission. Please try again.")
            return render_template('signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)

@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(form.data['username'], form.data['password'])
            if user:
                session['user_id'] = user.id
                flash("You've successfully logged in!")
                return redirect(url_for('users.welcome'))
        flash("Invalid credentials. Please try again.")
    return render_template('login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
~~~~

Now in our `base.html` we can list all of our flashed messages:

~~~~
{% for message in get_flashed_messages() %}
    {{ message }}
{% endfor %}
~~~~

For more on flash messages, check the [docs](http://flask.pocoo.org/docs/0.11/patterns/flashing/).

### Adding an `ensure_logged_in` decorator

With our app now manipulating the session, we have a way to verify whether or not somebody is logged in. We can now create a decorator to ensure someone is logged in (you can place this in the `views.py` file):

~~~~
from functools import wraps

def ensure_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please log in first")
            return redirect(url_for('users.login'))
        return fn(*args, **kwargs)
    return wrapper
~~~~

If we decorate the welcome route with `ensure_logged_in`, you should see find that you can no longer see the welcome page if you're signed out!

~~~~
@users_blueprint.route('/welcome')
@ensure_logged_in
def welcome():
    return render_template('welcome.html')
~~~~

At this point, we should also probably create a `logout` method that allows us to clear the session. We clear elements from the session using the `pop` method:

~~~~
@users_blueprint.route('/logout')
def logout():
  session.pop('user_id', None)
  flash('You have been signed out.')
  return redirect(url_for('users.login'))
~~~~

At this point, you should have a working mechanism for logging in and out, along with proper authentication for the welcome page!

#### current_user, before and after requests, and g

In Flask, there exists an object called `g`, which we can import. `g` is a global object that can be passed from route to route. Wait a second...this sounds exactly like the session! It is very similar, except `g` persists for **only one** request. So when would we use it?

The answer is when we want to write "hooks" or triggers for something to happen before or after the route. We can do this using the `before_request` or `after_request` decorator. In our case we would like all of our views to have access to a property called `current_user`, which is the user who is logged in. This is very useful for view logic and is commonplace in applications. Let's see how we could create a `current_user`.

~~~~
@users_blueprint.before_request
def current_user():
    if session.get('user_id'):
        g.current_user = User.query.get(session['user_id'])
    else:
        g.current_user = None
~~~~

You can now customize the view to show the user's username on the welcome screen. Try it out!

### Adding an `ensure_correct_user` decorator

Now that we have authentication, let's add another decorator for proper authorization. It would be pretty bad if users could edit other users, so anytime that we accept a parameter of `id` (show, edit, update, delete), let's make sure we are doing this **only** for the current user (the user who is logged in).

~~~~
from functools import wraps

def ensure_correct_user(fn):
    # make sure we preserve the corrent __name__, and __doc__ values for our decorator
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # in the params we have something called id, is it the same as the user logged in?
        if kwargs.get('id') != session.get('user_id'):
            # if not, redirect them back home
            flash("Not Authorized")
            return redirect(url_for('users.welcome'))
        # otherwise, move on with all the arguments passed in!
        return fn(*args, **kwargs)
    return wrapper
~~~~

You'll use this decorator in the exercises for this chapter.

### Cookies

We've seen how to use the session to add some state to our web application, and we've talked about how Flask's implementation of the session uses signed cookies. But it's also possible to achieve the same functionality using cookies directly. This isn't syntax you'll be using in your applications for this course, so this section isn't essential, but if you're curious about another approach, read on.

Cookies are smaller pieces of information that is stored on the browser. You can read more about cookies with Flask [here](http://flask.pocoo.org/docs/0.11/quickstart/#cookies). Cookies are commonly used to store `user_id`s as well as for analytics and "remember me" storage.

#### Reading cookies:

Reading cookies is a breeze. All we need to do is pull the data from the request object, which we import from Flask.

~~~~
from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.
    # after doing something with that value...
    return "All done!!"
~~~~

#### Setting cookies:

In order to set a cookie, we need to import the `make_response` function from Flask. We first need to make a response (render / redirect etc.) and then set a cookie to respond with:

~~~~
from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('username', 'eschoppik')
    return resp
~~~~

For more on sessions vs. cookies, check out [this](http://stackoverflow.com/questions/6253633/cookie-vs-session) StackOverflow question.

### Screencast

If you'd like to see an example of adding authentication and authorization to a Flask application, feel free to watch the screencast below.

Screencast: https://vimeo.com/244964772

### Exercise

Complete the [Hashing Sessions](https://github.com/rithmschool/python_curriculum_exercises/tree/master/Unit-02/03-hashing-sessions) exercise.

When you're ready, move on to [Authentication with Flask Login](/courses/intermediate-flask/authentication-with-flask-login)