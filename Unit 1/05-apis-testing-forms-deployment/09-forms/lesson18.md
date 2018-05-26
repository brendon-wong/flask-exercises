### Objectives:

By the end of this chapter, you should be able to:

*   Compare and contrast client and server side validation
*   Explain what a CSRF attack is and how it can be prevented
*   Explain what form hijacking is and how it can be prevented
*   Include FlaskWTF for validation and CSRF protection

So far we've been building our forms with some standard HTML, but unfortunately we have been neglecting any kind of validation!

### Client Side vs Server Side validation

Form validation is very common and quite important. When you ask for someone's phone number, you want to ensure that what they type represents a valid phone number. Same thing goes for email addresses, credit card numbers, and so on.

There are two ways to verify form information: either on the client, or on the server. Client-side validation is definitely helpful; there are even a lot of validation tools available out of the box in HTML5. (To read more about this, check out [MDN](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Forms/Data_form_validation).)

However, it is **essential** to validate your inputs on the server side. Validation on the client side is strictly for a better user experience and can easily be bypassed. If you only validate on the client side, you are opening yourself up to all kinds of malicious attacks. Without server side validation, someone could make themselves an admin of your site, try to delete other users, and so on.

To make server side validation a breeze, we can use the Flask WTF module.

### Our First Form

Let's create a new Flask project and explore how WTForms works with Flask.

~~~~
mkvirtualenv flask-forms
pip install flask flask-wtf
touch {forms,app}.py
~~~~

Inside of the `forms.py` let's create our first form.

~~~~
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, validators

class SignupForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    favorite_number = IntegerField('Favorite Number')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    newsletter = BooleanField('Sign me up for your newsletter!')
~~~~

Let's now create a little Flask app that makes use of this form. We'll only have two pages: a sign up page, and a welcome page for people who have signed up. Here's the `app.py`:

~~~~
from flask import Flask, request, redirect, url_for, render_template, flash
from forms import SignupForm

app = Flask(__name__)

@app.route('/signup', methods=['GET','POST'])
def signup():
    # request.form will be empty on a GET request, but populated on a POST request since it will contain values that a user has entered
    form = SignupForm(request.form)
    # let's first see if it is a post request
    if request.method == 'POST':
        # now we can use the WTForms validate method to see if we have passed our validations for the form we created in forms.py. This method returns True or False
        if form.validate():
          # we will cover flash messages more, but they are a one time message that is displayed to the user of our application
          flash("You have succesfully signed up!")
          return redirect(url_for('welcome'))
    # if the method is a GET - or if form.validate() returns False, our form will contain a dictionary called errors which contain the error messages to display to the user
    return render_template('signup.html', form=form)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
~~~~

Notice that we're setting a flash message if the form is validated. We'll talk more about flash messages later on; for now, you can think of them as short messages to display to the user based on some action.

Next we need to write some HTML.

### Displaying a form in a view

Create a `templates` folder, and inside of it let's create three files: `base.html`, `signup.html`, and `welcome.html`. The `base` should look quite familiar:

~~~~
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Introduction</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
~~~~

Next, we need to learn how to display our form in our view. Notice that in our `app.py` we are passing our form into the `render_template` function so that we have access to a `form` variable in the view. Here's what that might look like in our `signup.html`:

~~~~
{% extends 'base.html' %}

{% block content %}

<form method="POST" action="{{url_for('signup')}}">
  {% for field in form %}
  <p>
    {{ field.label }}
    {{ field }}
    <span>
      {% if field.errors %}
        {% for error in field.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  {% endfor %}
  <button type="submit">Sign up!</button>
</form>

{% endblock %}
~~~~

Finally, let's add to our `base.html`, which includes some logic around how to deal with the flash message set by our server:

~~~~
{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for message in messages %}
      <p>{{ message }}</p>
    {% endfor %}
  {% endif %}
{% endwith %}
~~~~

And now inside of our `welcome.html`, we can simply place the following and still see our flash messages. Make sure to put the above logic in your `base.html` since you'll want your flash messages to appear on any page that they are sent.

~~~~
{% extends 'base.html' %}

<h1>Welcome to the app!</h1>

{% block content %}

{% endblock %}
~~~~

At this point, you can go to `localhost:3000/welcome` to see the welcome page. However, if you try to access `/signup` you'll get an error:`KeyError: 'A secret key is required to use CSRF.'`

What does this mean, and how do we resolve the error? To answer this question, we need to understand an important concept in web security: CSRF.

### CSRF

One of the most common web attacks is **C**ross **S**ite **R**equest **F**orgery, or CSRF. In this attack, the hacker creates a form that looks real, and when users enter their credentials, the hacker captures the values in order to make malicious requests on that user's behalf. Before you continue, make sure to watch [this video](https://www.youtube.com/watch?v=vRBihr41JTo) to really develop an understanding of why this is such a real problem.

The idea here is that once a user is authenticated, a cookie is set in the browser to remember that the user has logged in. While this is great, there's a real security issue here.

Imagine you've logged into to some website (say it's your local bank). Once you're logged in, a cookie has been sent to your browser from the bank's website and when you visit the website, you don't have to log in. So everything is going well until you head over to another website which has been made by someone malicious.

The second that you enter that site, a POST request is sent (via AJAX) to the bank's website to transfer some money to another account. If the bank's website is insecure, it will simply think that this is just the user who logged in, that has decided to transfer some money to another account! This is pretty terrifying as you can trigger CSRF attacks without the user even having to click or submit anything!

In order to prevent CSRF attacks, a token is usually sent from the server when the form is rendered and if that token is not sent back to the server from the form when it is submitted, a 422 (unprocessable entity) error will be thrown.

One of the benefits of Flask-WTF is that forms are enabled with CSRF protection by default. However, in order to generate the token, we need to set a secret key on the server.

For some examples of CSRF, check out [this](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) article.

### Secret Keys

In order to create a CSRF token, we need to first have a "secret key" on the server. This "secret key" is simply a string that is used to encrypt data that is stored on the server (we call that the session). This secret key is used to send and decrypt the CSRF token to make sure it is valid. This secret key can be configured on your server like this.

~~~~
app.config['SECRET_KEY'] = 'any string works here'
~~~~

But this is bad as well! If someone gets access to our server, they can see this key and decrypt tokens on their own! Ideally we need some way of hiding this variable. We do this using `environment variables`.

When using `virtualenv` we have access to a hook called `postactivate`, which runs after the environment is created. Inside of here we can `export` variables for our environment. So let's run `code $VIRTUAL_ENV/bin/postactivate` and we should see a file where we can export values. Now let's add `export SECRET_KEY=shhhh` and save the file, and now we can change our `app.py` to this:

~~~~
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
~~~~

You might also need to `deactivate` your virtual environment and `workon` it again, as it won't be aware of changes to the `postactivate` file when you're already working on it.

Now if someone gets access to our server, they still won't be able to see what our secret key is!

At this point, you should be able to sign up successfully. And when you do, you should see the flash message on the welcome page!

For more on CSRF and Flask, check out the [docs](http://flask-wtf.readthedocs.io/en/stable/csrf.html).

### Hiding the CSRF Token when rendering a form

Finally, you may notice that when you iterate over the fields in the form, the hidden input with the CSRF token is included, you'll want to ignore that input when you're iterating. Here's how we could do that with a little bit of conditional logic!

~~~~
{% extends 'base.html' %}

{% block content %}

<form method="POST" action="{{url_for('signup')}}">
  {{form.hidden_tag()}}
  {% for field in form if field.widget.input_type != 'hidden'%}
  <p>
    {{ field.label }}
    {{ field }}
    <span>
      {% if field.errors %}
        {% for error in field.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  {% endfor %}
  <button type="submit">Sign up!</button>
</form>

{% endblock %}
~~~~

### Using a Database with WTForms

In the example above, we are working with a pretty simple example, but when we add SQLAlchemy in the mix, we have to be very mindful about one thing. **The variables you create in your forms.py should always correspond to the columns in your database** - what do we mean by that?

Let's imagine we had the following model:

~~~~
class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def __init__(self, first_name, last_name)
        self.first_name = first_name
        self.last_name = last_name
~~~~

If we wanted to build a form that we could use for creating or editing an author, here's what that **must** look like!

~~~~
class AuthorForm(FlaskForm):

    # notice that these variables first_name and last_name are the exact same as in our model above
    # this will make getting data from the form much simpler so try to always make those match up.
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
~~~~

### Passing values to a form when editing

Very commonly you'll want to pass in exisiting values you can use a keyword argument of `obj` and pass an object for prepopulated values. You can read more about that [here](http://wtforms.readthedocs.io/en/latest/forms.html).

That might look something like this (imagine we are working with authors as our resource):

~~~~
@app.route('/authors/<int:id>/edit')
def edit(id):
    found_author = Author.query.get(id)
    form = AuthorForm(obj=found_author)
    return render_template('edit.html', form=form)
~~~~

### One BIG gotcha with CSRF

Hopefully you're now starting to see why CSRF is such an issue and when we edit or create we can pass our form to a Jinja template and use `form.hidden_tag()` or `form.csrf_token` (`form.hidden_tag()` is more commonly used) to display the token - and that's great!

But there's one more kind of form that we are not securing. Remember that when you delete a resource, we still need a form, which means we **MUST** have CSRF protection for that form.

So how do we add a CSRF token to our forms when deleting? There are two options.

1.  Create an empty form using WTForms and pass that to the view
2.  Configure WTForms to allow you to pass a CSRF token and then validate seperately in your forms.

So which one should you use? The short answer is that step 1 will be much faster, but we will show both.

### Validating CSRF on Delete by Creating an Empty Class

In order to pass `form.hidden_tag()` to our template, we need an instance of a form. So in our `forms.py` we would add

~~~~
class DeleteForm(FlaskForm):
    # since we do not have any fields in our form, we will just pass here
    # we are only creating this class so we can inherit from FlaskForm and get built-in CSRF protection
    pass
~~~~

In our `app.py` we would then have something like this

~~~~
@app.route('/authors/<int:id>/', methods=["GET, DELETE", "PATCH"])
def show(id):
    found_author = Author.query.get(id)
    if request.method == b'PATCH':
      # notice for editing/creating we use a different form!
      form = AuthorForm(request.form)
      if form.validate():
        # normal edit logic
        found_author.first_name = form.data.first_name
        found_author.last_name = form.data.last_name
        db.session.add(found_author)
        db.session.commit()
        flash('Edited Successfully!')
        return redirect(url_for('index'))
      else:
        # if we fail to edit, show the edit page again with error messages and values that the user has typed in!
        return render_template('edit.html', form=form)
    if request.method == b'DELETE':
      # even though our delete form just has a button, there still is some information in request.form - the CSRF token!
      delete_form = DeleteForm(request.form)
      # just make sure they did not tamper with the CSRF token or do something malicious
      if delete_form.validate():
        # now that CSRF has been validated, go ahead and delete then redirect back!
        db.session.delete(found_author)
        db.session.commit()
        flash('Author Deleted!')
        return redirect(url_for('index'))
      # if they did, or if it is a GET request, just render the show page
    return render_template('show.html', delete_form=delete_form, found_author=found_author)
~~~~

Finally, here is what our `show.html` page might look like

~~~~
{% extends 'base.html' %}

{% block content %}
  <h1>Hi {{found_author.first_name}} {{found_author.first_name }}</h1>
  <form action="url_for('show')?_method=DELETE" method="POST">
    {{delete_form.hidden_tag()}}
    <input type="submit" value="X">
  </form>
{% endblock %}
~~~~

And now we have CSRF protection for our DELETE form! This might seem like a lot to add, but it is **essential** for securing your application.

### Validating CSRF on Delete by Configuring CSRF Protect

Instead of creating an empty form, we can take a longer approach by first ensuring that our application includes CSRF protection (something we normally get by inheriting from FlaskForm).

In our `app.py` make sure to include this import and then create an instance of the class with our `app` variable.

~~~~
from flask_wtf.csrf import CSRFProtect # add csrf protection without creating a FlaskForm (for deleting)

app = Flask(__name__)
csrf = CSRFProtect(app)
~~~~

What this gives us is something we can add to our Jinja templates called `csrf_token`. Here's what our `show.html` page might look like:

~~~~
{% extends 'base.html' %}

{% block content %}
  <h1>Hi {{found_author.first_name}} {{found_author.first_name }}</h1>
  <form action="url_for('show')?_method=DELETE" method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token()}}"/>
    <input type="submit" value="X">
  </form>
{% endblock %}
~~~~

So far this seems good! However, we need to add quite a bit of validation in our `app.py` - here is what a route for `/users/<int:id>` might look like:

~~~~
# add the top of your code make sure you include this now
  # validate_csrf is a function used to make sure the CSRF token is authentic
  # ValidationError is what is raised if the CSRF validation fails
from flask_wtf.csrf import validate_csrf, ValidationError

@app.route('/authors/<int:id>/', methods=["GET, DELETE", "PATCH"])
def show(id):
    found_author = Author.query.get(id)
    if request.method == b'PATCH':
        # notice for editing/creating we use a different form!
        form = AuthorForm(request.form)
        if form.validate():
          # normal edit logic
          found_author.first_name = form.data.first_name
          found_author.last_name = form.data.last_name
          db.session.add(found_author)
          db.session.commit()
          flash('Edited Successfully!')
          return redirect(url_for('index'))
        else:
          # if we fail to edit, show the edit page again with error messages and values that the user has typed in!
          return render_template('edit.html', form=form)
    if request.method == b"DELETE":
        try: # validate_csrf will raise an error if the token does not match so we need to catch it using try/except
          validate_csrf(request.form.get('csrf_token'))
          db.session.delete(found_author)
          db.session.commit()
          return redirect(url_for('owners.index'))
        except ValidationError: # if someome tampers with the CSRF token when we delete an owner
          return render_template('owners/show.html', found_author=found_author)
    return render_template('owners/show.html', found_author=found_author)
~~~~

In the code above, we are trying to run our validate_csrf method which either raises an error if validation fails or returns `None` if the validation is successful. If it returns `None` we delete the author - otherwise we catch the error and render the show page again.

### Form Hijacking

Another common security risk when building forms is form hijacking. Let's imagine we have the following form:

~~~~
<form action="/users" method="POST">
    <input type="text" name="username">
    <input type="submit" value="Create User">
</form>
~~~~

This form seems pretty harmless, but what happens if someone opens the chrome dev tools and edits the HTML to look like this?

~~~~
<form action="/users" method="POST">
    <input type="text" name="username">
    <input type="text" name="is_admin" value="true">
    <input type="submit" value="Create User">
</form>
~~~~

If that user submitted the form, what would happen if you actually had a column in your database called "is_admin"? A user could hypothetically create an account as an admin! Even though this may not be likely, it's incredibly dangerous. We need to make sure users can not hijack forms! On the server, it is very important to not just accept ALL parameters that a user can enter in a form, but be specific with the parameters that we want.

Flask-WTF fixes this problem, because the only fields it pays attention to are attributes in the form class that you define. (In the example above, this means `name`, `email`, `favorite_number`, `password`, `confirm`, and `newsletter`.) If you try to create any other inputs on the client side, they'll simply be ignored.

### Fields

As you've seen, WTForms has quite a few fields you can use when building your forms:

~~~~
IntegerField()
StringField()
TextInput()
PasswordField() # input with type password
BooleanField() # checkbox
FormField(AnotherFormClass) # for nesting forms
SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
~~~~

Here is what a sample form for resetting a password could look like:

~~~~
class ChangePassword(Form):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
~~~~

You can learn more about these [here](http://wtforms.readthedocs.io/en/latest/fields.html)

### Validators

Each of your fields can contain a list of validators. Here are some common ones:

~~~~
DataRequired(message='Custom Message Here') # require that something exists in the input
Email(message='Custom Message Here') # validate an email
EqualTo(fieldname, message='Custom Message Here') # make sure values are equal
~~~~

You can learn more about these, including validating a range or URL, [here](http://wtforms.readthedocs.io/en/latest/validators.html). You can also write your own custom validators for re-use:

~~~~
def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 50 characters')

class MyForm(Form):
    name = StringField('Name', [InputRequired(), my_length_check])
~~~~

### Screencast

If you'd like to see an example of adding WTForms to a Flask application, feel free to watch the screencast below.

Screencast: https://www.youtube.com/watch?v=UU0SVs4FekM

### Exercise

Complete the [WTForms](https://github.com/rithmschool/python_curriculum_exercises/tree/master/Unit-01/09-forms) exercise.

When you're ready, move on to [Deployment with Heroku](/courses/flask-fundamentals/flask-heroku-deployment)