## CRUD With Flask

### Objectives:

By the end of this chapter, you should be able to:

*   Explain what REST is and describe RESTful routing
*   Include flask modus for overriding the default HTTP method
*   Build a CRUD app in Flask
*   Include a stylesheet in a Flask application

Now that we have a solid understanding of the basics of Flasks, it's time to build some more powerful web applications. Before we do so, let's quickly review some key concepts relating to the internet.

### Key Definitions

**HTTP** \- The protocol that clients and servers use to communicate.

**Idempotent** \- An operation is idempotent if calling it multiple times yields the same result. For example, `GET` requests should be idempotent.

**CRUD** \- Shorthand for **C**reate, **R**ead, **U**pdate, and **D**elete. We often talk about implementing CRUD on a resource when building web applications.

**Resource** \- A `noun` that we operate on. An application can have many resources, but each resource will have its own set of routes and CRUD operations. For example, `users` and `tweets` are two examples of resources for Twitter.

### Review HTTP Verbs

*   `GET` \- for retrieving information or sending information via the query string
*   `POST` \- for sending information via the body of the request
*   `PUT` \- for updating an entire resource
*   `PATCH` \- for updating a part of a resource
*   `DELETE` \- for removing a resource

### GET vs POST

*   `GET` is usually faster
*   `POST` is always more secure is information is not transmitted in the query string (the URL bar in the browser can be seen by anyone)
*   `GET` is idempotent; POST is not.

### REST

As applications grow larger and more developers work on them, structuring and naming things like routes becomes something that needs to be standardized. While REST is much more than route standardization (it is a standard for building web applications), one of the ideas is centering applications around resources and naming the routes for those resources appropriately (we call that RESTful routing).

Let's imagine that we have a web app with a resource of `students` (resources are ALWAYS in the plural). Here are what the HTTP Verb, RESTful routes and action look like.

`GET '/students'` -\> render a page called `'index.html'` (typically with information on all students)

`GET '/students/new'` -\> render a page called `'new.html'` (typically with a form to create a new student)

`GET '/students/:id'` -\> render a page called `'show.html'` (typically with information on the student with the given id)

`GET '/students/:id/edit'` -\> render a page called `'edit.html'` (typically with a form to edit the student with the given id)

`POST '/students'` -\> create a new resource, then redirect.

`PATCH '/students/:id'` -\> find a resource by the id, update it, then redirect.

`DELETE '/students/:id'` -\> find a resource by the id, remove it, then redirect.

The filenames `index`, `new`, `show` and `edit` are NOT required, but are convention when working with RESTful routing and are highly encouraged (especially by larger frameworks like Ruby on Rails).

### Getting started

Let's build our first CRUD app with Flask! To get started we first need a resource: let's use toys. Since we will be creating toys, we'll start by making a file called `toy.py` which will store a simple toy class. In order to make sure that we can uniquely identify each toy, we will add a property called `id` that increments by one anytime a toy is created

~~~~
class Toy():

    count = 1

    def __init__(self,name):
        self.name = name
        self.id = Toy.count
        Toy.count += 1
~~~~

Now let's create an `app.py` file to start our server with some sample data. When the user visits the route `/toys`, let's start by creating an index route where we will return a template that shows all of our toys.

~~~~
from flask import Flask, render_template
from toy import Toy

app = Flask(__name__)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys')
def index():
    return render_template('index.html', toys=toys)
~~~~

### Index

In order for that first route to work, we now need an `index.html` file! First we will need a `templates` folder; inside let's create a `base.html` and an `index.html`. Let's start with the `base.html`:

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CRUD Time</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
~~~~

Now let's add to our `index.html` and inherit from `base.html`. Inside of this template, let's iterate over our list of toys that are being sent to the template from Flask. Try this on your own first!

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

Now let's start the server using `flask run` and head over to `localhost:5000/toys`. We should see all of our toys here!

### New

Now that we can show all of our toys, lets create a route to render a page with a form for creating a new toy. This route is not responsible for **actually** creating the toy, that's for later. Let's call this route `new`.
~~~~
from flask import Flask, render_template
from toy import Toy

app = Flask(__name__)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys')
def index():
    return render_template('index.html', toys=toys)

@app.route('/toys/new')
def new():
    return render_template('new.html')
~~~~

Now let's create our `new.html` file with a form. This form should have one input for the name of the new toy we are making. In order to send data to our server, we have to add a `name` attribute in our form. This is how we will access the value of whatever the user types in for the name of the toy. When the form is submitted, we will reuse our index function but with a different HTTP verb: this time, we'll use a POST request.

~~~~
{% extends 'base.html' %}
{% block content %}
    <form action="{{url_for('index')}}" method="POST">
        <input type="text" name="name">
        <input type="submit" value="Add a toy">
    </form>
{% endblock %}
~~~~

So we have a form, but if you try to create a new toy with this form, you should see a Method Not Allowed error in the browser. This is because we haven't set up our `/toys` route to accept POST requests! And even if it could, we haven't told it how to handle such requests by updating the list of toys. Let's make those modifications next:

### Create

Before we discuss what the modified route will look like, we should think about what we want to happen when we submit the form. Once we have finished creating a Toy, it would be a bit silly to render another HTML page telling us that we just created a toy. Instead, it would make more sense to go back to the `index` page and see an updated list of all the toys. So, how can we make another request to send us the `index` page? To do that we have to introduce a concept called "redirecting."

### Redirect

A redirect is actually two separate requests:

1.  First, the server sends a response with a header called 'location' with a value that is a `route`
2.  The browser receives the response and immediately issues a new request to the route provided in the `location` header
3.  If the route exists on the server, the server responds accordingly (or returns a 404 status code (page not found)).

To do this with Flask, we need to import `redirect`. We will also import `url_for` so that we do not have to "hard code" our routes, as well as `request` which we will use to collect data from a form.

~~~~
from flask import Flask, render_template, redirect, url_for, request
from toy import Toy

app = Flask(__name__)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # gather the value of an input with a name attribute of "name"
        toys.append(Toy(request.form['name']))
        # respond with a redirect to the route which has a function called "index" (in this case that is '/toys')
        return redirect(url_for('index'))
    # if the method is GET, just return index.html
    return render_template('index.html', toys=toys)

@app.route('/toys/new')
def new():
    return render_template('new.html')
~~~~

Notice that we had to specify in our `@app.route` for toys that our application should accept both GET and POST. Then, inside of `index`, we can handle each case separately.

Try it out - you should now be able to add new toys inside of your application!

### Show

Now that we are able to create new toys, let's make a route to show some additional information about the toys. In order for this to work, we are going to need a way to find individual toys by their id. Let's make a route that includes a dynamic parameter called `id` which is an integer. Let's call the function that this route triggers `show`.

~~~~
from flask import Flask, render_template, redirect, url_for, request
from toy import Toy

app = Flask(__name__)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        toys.append(Toy(request.form['name']))
        return redirect(url_for('index'))
    return render_template('index.html', toys=toys)

@app.route('/toys/new')
def new():
    return render_template('new.html')

@app.route('/toys/<int:id>')
def show(id):
    # find a toy based on its id
    for toy in toys:
        if toy.id == id:
            found_toy = toy
    # Refactor the code above using a list comprehension!

    return render_template('show.html', toy=found_toy)
~~~~

Now let's create a simple page that shows more information about the toy. Let's also add a link for us to edit a toy. We will call this function `edit`, and since we need to specify which toy to edit, we will pass an `id` of a toy to this `url`.

~~~~
{% extends 'base.html' %}
{% block content %}
    <h1>Let's see some more information about this toy!</h1>
    <p>
        The name of the toy is {{toy.name}} - it's a pretty great one.
    </p>
    <a href="{{url_for('index')}}">See all the toys</a>
    <br>
    <a href="{{url_for('edit', id=toy.id)}}">Edit this toy</a>
{% endblock %}
~~~~

Of course, with that second link present, we'll get an error on this page, because we don't have a route for editing. Let's work on that next.

### Edit

In order to edit a toy we need to first make sure we have a route that renders a form for editing. Before we can edit a toy, though, we first need to render a page with a form to edit the toy.

~~~~
from flask import Flask, render_template, redirect, url_for, request
from toy import Toy

app = Flask(__name__)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        toys.append(Toy(request.form['name']))
        return redirect(url_for('index'))
    return render_template('index.html', toys=toys)

@app.route('/toys/new')
def new():
    return render_template('new.html')

@app.route('/toys/<int:id>')
def show(id):
    # Refactored using a list comprehension!
    found_toy = [toy for toy in  toys if toy.id == id][0]
    # Refactor the code above to use a generator so that we do not need to do [0]!
    return render_template('show.html', toy=found_toy)

@app.route('/toys/<int:id>/edit')
def edit(id):
    # Refactored using a list comprehension!
    found_toy = [toy for toy in  toys if toy.id == id][0]
    # Refactor the code above to use a generator so that we do not need to do [0]!
    return render_template('edit.html', toy=found_toy)
~~~~

Now let's create a page called `edit.html` for us to edit a toy. When this form is submitted we will go back to the route called show, but with a method of "PATCH". We also would like our form to be pre-filled with the values we have for the toy, so let's use the `value` attribute on our input for that.

~~~~
{% extends 'base.html' %}
{% block content %}
    <form action="{{url_for('show', id=toy.id)}}?_method=PATCH" method="POST">
        <input type="text" name="name" value="{{toy.name}}">
        <input type="submit" value="Add a toy">
    </form>
{% endblock %}
~~~~

If you look at the form tag, you may notice that something funky is going on. Why are we setting the method to be PATCH in the action, but POST in the method? Read on to find out!

### Flask modus

Unfortunately, forms can only send GET and POST requests. In order to override the default methods, we need to use `flask_modus` to override the HTTP verb in headers and query string.

`pip install flask-modus`

Let's now import what we need. In order to be able to override the default form methods, we need to pass our application into the `Modus` function:

~~~~
from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from toy import Toy

app = Flask(__name__)
modus = Modus(app)

# ...
~~~~

~~~~
{% extends 'base.html' %}
{% block content %}
    <form action="{{url_for('show', id=toy.id)}}?_method=PATCH" method="POST">
        <input type="text" name="name" value="{{toy.name}}">
        <input type="submit" value="Add a toy">
    </form>
{% endblock %}
~~~~

### Update

At this point our HTML is in pretty good shape, but we need to tell our server how to handle PATCH requests. We'll do this by letting `/toys/<int:id>` accept both GET and PATCH:

~~~~
from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from toy import Toy

app = Flask(__name__)
modus = Modus(app)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        toys.append(Toy(request.form['name']))
        return redirect(url_for('index'))
    return render_template('index.html', toys=toys)

@app.route('/toys/new')
def new():
    return render_template('new.html')

@app.route('/toys/<int:id>', methods=["GET", "PATCH"])
def show(id):
    # Refactored using a generator so that we do not need to do [0]!
    found_toy = next(toy for toy in  toys if toy.id == id)

    # if we are updating a toy...
    if request.method == b"PATCH":
        found_toy.name = request.form['name']
        return redirect(url_for('index'))
    # if we are showing information about a toy
    return render_template('show.html', toy=found_toy)

@app.route('/toys/<int:id>/edit')
def edit(id):
    # Refactored using a generator so that we do not need to do [0]!
    found_toy = next(toy for toy in  toys if toy.id == id)
    return render_template('edit.html', toy=found_toy)
~~~~

Note that when you're using `flask-modus` and examining the `request.method`, you'll get back a bytes literal, not a string. That's why you need to compare to `b"PATCH"`, not `"PATCH"`. If you want to learn more about the distinction between bytes and strings in Python 3, check out [this](http://eli.thegreenplace.net/2012/01/30/the-bytesstr-dichotomy-in-python-3) blog post.

### Delete

By now you should be able to perform CRU completely within your browser. Next, let's put the D into CRUD by building out the delete functionality.

In our `edit.html` we are going to add another form to delete a toy. This is done with a form since we need to make a DELETE request.

~~~~
{% extends 'base.html' %}
{% block content %}
    <form action="{{url_for('show', id=toy.id)}}?_method=PATCH" method="POST">
        <input type="text" name="name" value="{{toy.name}}">
        <input type="submit" value="Add a toy">
    </form>

    <form action="{{url_for('show', id=toy.id)}}?_method=DELETE" method="POST">
        <input type="submit" value="Delete a toy">
    </form>
{% endblock %}
~~~~

Back in our `app.py` let's add the necessary code to find a toy, remove it, and then redirect back to the `index` route. We can add all of this functionality to our existing `show` function:

~~~~
@app.route('/toys/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    # Refactored using a generator so that we do not need to do [0]!
    found_toy = next(toy for toy in  toys if toy.id == id)

    # if we are updating a toy...
    if request.method == b"PATCH":
        found_toy.name = request.form['name']
        return redirect(url_for('index'))

    if request.method == b"DELETE":
        toys.remove(found_toy)
        return redirect(url_for('index'))
    # if we are showing information about a toy
    return render_template('show.html', toy=found_toy)
~~~~

With that, you should have a working CRUD app! Congratulations.

### Styling our application

Our toy app is completely functional now, but unfortunately it doesn't look too hot. Let's fix this by adding some CSS to our application!

To add CSS, JavaScript, or any other static assets to a Flask app, you'll first need to create a directory called `static` at the root of your project. Inside of `static`, create a file called `style.css`.

Here's some default styling for you:

~~~~
li {
  font-size: 25px;
}

h1,
p {
  text-align: center;
}

body::after {
  content: "";
  background: url(http://cinematically.net/wp-content/uploads/2014/08/toys_poster.jpg);
  opacity: 0.3;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  position: absolute;
  z-index: -1;
}
~~~~

(Want to know what's going on with that `body::after` selector? Check out [this](https://css-tricks.com/snippets/css/transparent-background-images/) article.)

Finally, we need to link to our stylesheet from inside of `base.html`:

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CRUD Time</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
~~~~

Beautiful!

### Screencast

If you'd like to see an example of building a CRUD application with a list, feel free to watch the screencast below.

Screencast: https://www.youtube.com/watch?v=LPdWU9VF-Po

When you're ready, move on to [Flask Fundamentals Exercises](/courses/flask-fundamentals/flask-fundamentals-exercises)