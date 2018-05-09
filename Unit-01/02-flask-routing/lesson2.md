### Objectives:

By the end of this chapter, you should be able to:

*   Create multiple routes with Flask
*   Capture URL parameters and define their types

In the previous section, we saw how to start a server with Flask, add a couple of routes, and make sure our server is listening for changes using `FLASK_DEBUG=1`. Now let's build off of that knowledge and add some more dynamic routes.

First, let's make a new virtual environment and ensure Flask is installed.

mkvirtualenv flask-routing
workon flask-routing
pip install flask

Let's make an `app.py` file

from flask import Flask

app = Flask(\_\_name\_\_)

@app.route('/')
def hello():
    return "Hello!"

@app.route('/hi')
def hi():
    return "Hi!"

@app.route('/bye')
def bye():
    return "Bye!"

As before, we can start this application by running `FLASK_APP=app.py FLASK_DEBUG=1 flask run` and heading to `localhost:5000` in the browser. You should see that as you change the location in the url bar from `localhost:5000` to `localhost:5000/hi` to `localhost:5000/bye`, the message on the page changes as well.

### Adding url parameters

Right now our application has three routes in the `app.py` file. But modern web applications may have thousands or even millions of routes. On Twitter, for example, you can get a route specific to an individual tweet! Does this mean that Twitter has to maintain an `app` file with billions of individual routes in it? Thankfully, the answer is no.

Instead, something you will commonly do when creating routes is allow for dynamic values to be passed to them. Right now our routes are pretty fixed. Our routes are `/`, `/hi` and `/bye` and they will always respond with the same thing when we make a request to those routes. But what if we could dynamically change the response based on the route the user requests? For instance, if a request is made to `localhost:3000/name/elie`, the server responds with the text "The name is elie" and if a request is made to `localhost:3000/name/tim`, the server responds with the text "The name is tim". One way we might think of doing this is:

@app.route('/name/elie')
def elie():
    return "The name is elie"

@app.route('/name/matt')
def matt():
    return "The name is matt"

But what happens when we want to do this for 1,000 people? We can't possibly write that many routes, so it would be really neat if we could just return **whatever** is passed after the `/name/`. If we do `/name/elie` it knows that the value we want is "elie"; if we do `/name/matt` the value we want is "matt," and so on.

To do this in Flask, we can create a URL parameter using `<NAME_OF_VARIABLE>` in  
our route.

from flask import Flask
app = Flask(\_\_name\_\_)

@app.route('/')
def home():
    return "Welcome!"

#let's make up a parameter called name. Its value is going to be WHATEVER someone requests, but we will respond with the string "The name is" along with the value in the URL.
@app.route('/name/<person>')
def say_name(person):
    return f"The name is {person}"

\# since all URL parameters are strings, we can convert them right away to another data type in our route definition
@app.route('/name/<int:num>')
def favorite_number(num):
    return f"Your favorite number is {num}, which is half of {num * 2}"

Notice that Flask is smart enough to determine how to handle the routing based on the type of the variable passed in to the URL: `/name/elie` gets handled by `say_name`, while `/name/1` gets handled by `favorite_number`. Moreover, we see that in the latter case, the number really is of type number, since we can double it and display the result on the page.

### Exercise

First, try to replicate the example above! There is a lot of value in building up the muscle memory for creating simple Flask applications, routes and understanding how URL parameters work.

After that, complete the[Flask Routing](https://github.com/rithmschool/python_curriculum_exercises/tree/master/Unit-01/02-flask-routing)exercise.

When you're ready, move on to [Templating with Jinja2](/courses/flask-fundamentals/templating-with-jinja2)