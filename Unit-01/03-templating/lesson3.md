## Templating with Jinja2

### Objectives:

By the end of this chapter, you should be able to:

*   Use Flask to respond by rendering HTML instead of plain text
*   Use Jinja2 as a server side templating engine
*   Pass values to a server side template with Flask and evaluate them with Jinja

### What is a template?

Very commonly, we want to send data from our server back to our client. In the olden days, servers often just held a collection of files; the client would request, say, an HTML file, and the server would send it over. Because these files were static and unchanged by the server, such sites are often referred to as _static sites_.

In more modern web development, instead of sending static data all the time, we often want to send _dynamic_ data, which may depend on which user is signed in, whether a user's account has expired, and so on. To do this we will be using the templating engine built into Flask, which is called Jinja2.

### Jinja2

Since Jinja2 comes with Flask we do not need to `pip install` anything and we can get started right away. To evaluate data from our server in our templates we use the `{% %}` notation and to print data we use `{{ }}`. (Not clear on the difference between evaluating and printing data in a template? Don't worry, we'll see an explicit example very soon.)

Let's start by first having Flask render HTML. To do so we must include `render_template` when importing from `flask`. Let's make an `app.py` and include the following:

~~~~
from flask import Flask, render_template # we are now importing just more than Flask!

app = Flask(__name__)

@app.route('/')
def welcome():
    names_of_instructors = ["Elie", "Tim", "Matt"]
    random_name = "Tom"
    return render_template('index.html', names=names_of_instructors, name=random_name)

@app.route('/second')
def second():
    return "WELCOME TO THE SECOND PAGE!"
~~~~

So what's happening above? Instead of just rendering plain text, we are rendering a template called `index.html` and we are passing some variables into the template. These variables are called `names` and `name` and their values are the `names_of_instructors` variable (`["Elie", "Tim", "Matt"]`) and `random_name` variable (`"Tom"`). Very commonly these keys and values will be named the same, but we are using different names to show the difference in this example.

Now in order to make sure that Flask can find our templates, we need to create a folder called `templates` and inside let's create our `index.html` file.

### Logic in templates

Now let's add the following into our `index.html` file.

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    {% for instructor_name in names %}
        <p>{{ instructor_name }}</p>
    {% endfor %}

    {% if name == 'Tom' %}
        <p>Hello {{ name }}!</p>
    {% endif %}
</body>
</html>
~~~~

We can iterate over lists using `for` with Jinja and use conditional logic with `if` statements! This means we can render the same HTML page and produce different views for different users. Our pages are now much more dynamic! Think about some applications for something like this: templating allows you to listing all of your friends on a social network, displaying information only if you are an admin, show a logout button if you are logged in, and more, all with just a small number of templates living on the server.

Note also that that only Python code inside of `{{ }}` gets printed to the page. You'll often see `for` loops and `if` statements defined inside of `{% %}`, since we want to evaluate that code, but it's only when we're inside the `if` or `for` blocks that we want to display something on the page (using `{{ }}`).

### Template Inheritance

One of the more powerful features of Jinja is the ability to use template inheritance, which means that one template can inherit from another. Let's see an example! First, let's create a file called `base.html`:

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
   {% block content %}
   {% endblock %}
</body>
</html>
~~~~

In another template (in the same directory), create a file called `title.html`:

~~~~
{% extends "base.html" %}
{% block content %}
<h1>This page has everything our base.html has!</h1>
{% endblock %}
~~~~

We can inherit from other templates using the `extends` keyword. This tremendously reduces our code duplication especially for things like headers and footers. To see this inheritance in action, add another route to your `app.py`:

~~~~
@app.route('/title')
def title():
    return render_template('title.html')
~~~~

### URL Helpers

Another great helper that Jinja has is the `url_for` helper which eliminates the need for hard coding a URL. This is very helpful when you have dynamically created URLs or don't always know the exact path. Let's imagine we are working in our `index.html` file and we would like an anchor tag to link to the route `/second`. We also know that in our `app.py` the function that is used to send a response to our server is called `second`. This is what we can place as the value for our `url_for()`!

~~~~
{% extends "base.html" %}
{% block content %}
    {% for name in names %}
        {{name}}
    {% endfor %}

    {% if name == 'Tom' %}
        <p>Hello Tom!</p>
    {% endif %}

    Tired of this page? Head over to <a href="{{url_for('second')}}">the second page!</a>
{% endblock %}
~~~~

### Getting data from the query string

When a user submits a form via a GET request, that form data can be captured from the query string. Flask makes this process a bit easier with a method called `request`. Let's see it in action. To begin, start with a simple form in a page called `first-form.html`:

~~~~
{% extends "base.html" %}
{% block content %}
    <form action="/data">
        <input type="text" name="first">
        <input type="text" name="last">
        <input type="submit" value="Submit Form">
    </form>
{% endblock %}
~~~~

To capture this data we can use `request` which we need to import from `flask` and access the `args` property inside request.

~~~~
from flask import Flask, render_template, request # we are now importing just more than Flask!

app = Flask(__name__)

@app.route('/')
def welcome():
    names_of_instructors = ["Elie", "Tim", "Matt"]
    random_name = "Tom"
    return render_template('index.html', names=names_of_instructors, name=random_name)

@app.route('/second')
def second():
    return "WELCOME TO THE SECOND PAGE!"

@app.route('/title')
def title():
    return render_template('title.html')

# we need a route to render the form
@app.route('/show-form')
def show_form():
    return render_template('first-form.html')

# we need to do something when the form is submitted
@app.route('/data')
def print_name():
    first = request.args.get('first')
    last = request.args.get('last')
    return f"You put {first} {last}"
~~~~

### Additional Resources

[https://realpython.com/blog/python/primer-on-jinja-templating/](https://realpython.com/blog/python/primer-on-jinja-templating/)

### Exercise

Complete the [Flask Templating](https://github.com/rithmschool/python_curriculum_exercises/tree/master/Unit-01/03-templating) exercise.

When you're ready, move on to [CRUD With Flask](/courses/flask-fundamentals/crud-with-flask)