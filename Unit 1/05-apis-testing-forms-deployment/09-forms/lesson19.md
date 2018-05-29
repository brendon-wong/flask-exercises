## Deployment with Heroku

### Objectives:

By the end of this chapter, you should be able to:

*   Deploy applications to Heroku
*   Configure and debug Heroku applications

### Start with a simple Flask application

Let's start in the terminal:

~~~~
mkdir deploy_flask
cd deploy_flask
mkvirtualenv flask-heroku
workon flask-heroku
pip install flask
createdb flask-heroku
~~~~

And create a simple `app.py` with the following:

~~~~
from flask import Flask
import os

app = Flask(\_\_name\_\_)

@app.route('/')
def hello():
    return "Hello World!"
~~~~

### Install Gunicorn

When we deploy an application in production, we will always want to use a server that is production ready and not meant for just development. The server we will be using is [gunicorn](http://gunicorn.org/) so let's make sure we run `pip install gunicorn`.

### Requirements.txt

When our application is deployed by Heroku, we need to tell heroku what packages to install. Heroku expects a file called `requirements.txt` where it will find all the necessary dependencies of our application. To create this file, we can simply run `pip freeze > requirements.txt`. It's a good idea to do this in general for projects you're working on, especially if your code is on GitHub; it's an easy way for other developers to identify which packages to install if they fork and clone your work!

### Procfile

When we push our code to Heroku, we need to tell Heroku what command to run to start the server. This command **must** be placed in a file called `Procfile`. Make sure this file does **not** have any extension and begins with a capital `P`. We can run the following command from the Terminal to do this `echo web: gunicorn app:app > Procfile`

### runtime.txt

To make sure you are using a certain version of Python on Herkou, add a file called `runtime.txt` and specify the version of Python you want to use. We can do this with `echo python-3.6.2 > runtime.txt`

### Deploying to Heroku

We first need to download the Heroku - you can do that with `brew install heroku`

Once you have installed it and created an account on [heroku.com](http://heroku.com), you should be able to run the following commands.

~~~~
git init
git add .
git commit -m "initial commit"
heroku login
heroku create NAME\_OF\_APP
git remote -v # make sure you see heroku
git push heroku master
heroku ps:scale web=1  # make sure you add a dyno (worker) to your application to create a process for heroku to run  
heroku open
~~~~

### Debugging a Heroku Application

To debug an application in production, our best bet is to take a look at the server logs using the following command:

~~~~
heroku logs -t
~~~~

Make sure you have another terminal window open to do this as it will show you the trailing logs (as new requests come in, it will change). This is very similar to what you would see in your terminal when developing locally. In the logs you will see requests coming in and how your server is responding. You will also find any errors here when your application crashes so make sure to run `heroku logs -t` if your application has crashed!

### Environment Variables

Now that we have an application set up, let's make sure we have an environment variable set so that we are not running in debug mode. Let's also add an environment variable for our SECRET_KEY for when we build secure forms.

~~~~
\# lets create an environment variable for our environment!
heroku config:set ENV=production
heroku config:set SECRET_KEY=shhhh
~~~~

### Setting up a postgres database

In order to use a production database, we need to have heroku create one for us using the following command.

~~~~
heroku addons:create heroku-postgresql:hobby-dev
~~~~

Now that we have a postgres database, we need to make sure that we are connecting to the correct database when in production!

~~~~
\# If we are in production, make sure we DO NOT use the debug mode
if os.environ.get('ENV') == 'production':
    \# Heroku gives us an environment variable called DATABASE_URL when we add a postgres database
    app.config\['SQLALCHEMY\_DATABASE\_URI'\] = os.environ.get('DATABASE_URL')
else:
    app.config\['SQLALCHEMY\_DATABASE\_URI'\] = 'postgres://localhost/flask-heroku'
~~~~

Since we are in different environments when developing versus in production, we'll need to use conditional logic to determine how our application runs. In production, we never ever want to have `debug=True` because if an error occurs, we do not want all our users seeing the entire stack trace and friendly flask debugger - that could be a real security vulnerability. The same goes for our database as well - in production we will be connecting to a different database.

### Migrations

If your apps have a database, you will have to run your migrations _on heroku_ in order to have all of the tables that your app needs. To run a command on the heroku machine, use `heroku run`. So to get your database setup, run:

~~~~
heroku run flask db upgrade
~~~~

### Refactoring conditional logic

As our applications grow, and we add more and more conditional logic for different environments, things can start to get messy. A good refactor for this is to actually use some principles from Object Oriented Programming - inheritance and polymorphism.

What we mean by this, is that we can create a base class with some initial configuration and create subclasses which inherit from the base class with slight modifications. To do this, we will create another file in the root of our application called `config.py` and then back in our `app.py` we will configure our application from the settings in `config.py`. You can read more about that [here](http://flask.pocoo.org/docs/0.11/config/#configuring-from-files).

Here's what our config.py might look like -

~~~~
import os

class Config():
    TESTING = False
    SQLALCHEMY\_DATABASE\_URI = 'postgres://localhost/flask-heroku'

class ProductionConfig(Config):
    SQLALCHEMY\_DATABASE\_URI = os.environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
~~~~

Notice here that we are creating a base class `Config` and then creating quite a few other subclasses for each of our environments, with some slight modifications.

Now in our `app.py`, we can refactor the following code to look like:

~~~~
\# one line to configure our application!
if os.environ.get('ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
    \# notice here that we are configuring from a file called "config" and a class inside called "ProductionConfig"
else:
    app.config.from_object('config.DevelopmentConfig')
    \# notice here that we are configuring from a file called "config" and a class inside called "DevelopmentConfig"
~~~~

As we have more and more differences between our environments, we can isolate that logic in a `config.py` file and remove any messiness from our `app.py`. Try to refactor your code to use a `config.py` file and use `app.config_from_object` to create your application settings!

### Adding Assets

When you include external files and assets, they MUST be served over `https`, otherwise Heroku will not serve the files.

### Screencast

If you'd like to see an example of deploying a Flask application, feel free to watch the screencast below.

Screencast: https://www.youtube.com/watch?v=nRiykxq0oHQ

### Exercise

Deploy two Flask applications that you've built in this unit!