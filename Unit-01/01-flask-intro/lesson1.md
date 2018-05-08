### Objectives:

By the end of this chapter, you should be able to:

*   Install `virtualenvwrapper` and create virtual environments
*   Use Flask to set up a simple server and respond with text

### Getting set up in a virtual environment

As you start working on more Python projects, you may find that managing dependencies becomes problematic. For example, you may start a project that uses version 2.x of some library, and later on you may start a new project and realize that version 3.x of the module is available. But this new version breaks things in your old project, so you need to either deal with a broken old project, or a new project with an old version of the library.

It would be better if we could separate out distinct environments for each Python project we worked on. That way, we wouldn't have to worry about dependencies in one project potentially interfering with other projects.

Thankfully, there's a way to set this up without much trouble in Python. The tool we'll be using is called `virtualenvwrapper`. Before we get started with any significant Python development, let's set up `virtualenvwrapper` so we can create separate environments for each project we'll be working on.

If you are on Windows, you can install the package [here](https://pypi.python.org/pypi/virtualenvwrapper-win)

### Installing `virtualenvwrapper`

pip3 install virtualenvwrapper  

In the event that your `$PATH` doesn't how to find your newly-installed `virtualenvwrapper`, let's also set up a link:

ln -s /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh  /usr/local/bin/virtualenvwrapper.sh

Next, in your `.zshrc` file add the following at the bottom:

export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

This determines where our virtual environments should live and also determines which version of Python we should be using. Finally, it specifies the location of `virtualenvwrapper`.

You can let Terminal know there's been a change to the `.zshrc` file by typing `source ~/.zshrc`. You now should be set up to create your first virtual environment!

To create our first virtual environment, you'll use the `mkvirtualenv` command:

mkvirtualenv first-env

Once you've created the environment, you should see the name of it appear on the left in Terminal. Now let's create a second environment!

mkvirtualenv second-env

You can switch between environments using the `workon` command.

workon first-env
workon second-env

If you want to see a list of all your current virtual environments, you can use the `lsvirtualenv -b` command (`-b` stands for "brief").

If you want to leave a virtual environment without switching to another one, you can simply type `deactivate` to exit the current environment. To permanently delete a virtual environment, you can use the `rmvirtualenv` command. Just know that you can't delete a virtual environment you're currently in; you'll need to switch to another environment or deactivate first. Try this out by creating a third virtual environment, then try to remove it.

One thing to note is that when you're in a virtual environment, you can just type `python` instead of `python3` to use Python 3. The default version of Python in these environments will be Python 3, because of this line in your `.zshrc` file:

export VIRTUALENVWRAPPER_PYTHON=/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

Similarly, you can just type `pip` instead of `pip3`!

To see how helpful these environments are, let's install something in one environment but not the other:

workon first-env
pip install bs4

(Recall that `bs4` is Beautiful Soup, the tool we used for web scraping in the last unit.)

To see a list of our dependencies, we can type `pip freeze`. Do this and you should see the following in Terminal:

beautifulsoup4==4.5.1
bs4==0.0.1

Now switch to `second-env` and type `pip freeze` again. You shouldn't see any output: Beautiful Soup was only installed in one environment!

Finally, if you ever need to locate these environments on your computer, they can be found in `~/.virtualenvs`. You should find a directory for each virtual environment. However, you should be able to manage these environments strictly using the commands that `virtualenvwrapper` gives you, so it shouldn't be necessary to manipulate things in the `.virtualenvs` directory directly.

### What is Flask?

Now that we know how to manage dependencies and create virtual environments for our projects, let's talk about one of the most important packages we'll be using in this course: Flask.

Flask is a micro-framework in Python. It allows us to easily start a server, and, when combined with other modules, build sophisticated applications. Flask is very easy to get started with so let's jump in! First we need to make a virtual environment:

mkvirtualenv first-flask-app
workon first-flask-app
pip install flask

Now let's create an `app.py` file. To begin, we'll just use the code from the [Flask docs](http://flask.pocoo.org/) (we've commented it up a bit):

\# from the flask library import a class named Flask
from flask import Flask

\# create an instance of the Flask class
app = Flask(\_\_name\_\_)

\# listen for a route to `/` - this is known as the root route
@app.route('/')
\# when this route is reached (through the browser bar or someone clicking a link, run the following function)
def hello():
    \# this \`return\` is the response from our server. We are responding with the text "Hello World"
    return "Hello World!"

Make sure we save our file. Next, in the terminal let's run `FLASK_APP=app.py flask run` and head over to [localhost:5000](localhost:5000) in the browser. You should see the text "Hello World" appear on the page!

Let's take a minute to understand what just happened. When you install `flask`, you gain access to a terminal command called `flask`, which allows you to do things like start your application from the command line. We'll see other uses for this command later on. Note that you have to tell `flask` where your application logic lives, which is why we specified `FLASK_APP=app.py` in the terminal command before typing `flask run`. For now, typing `flask run` on its own won't work - you'll get an error. We can clean this up a little later, but we'll live with it for now.

Note that if you're reading other Flask tutorials, you may have seen other ways to start your server. For example, you may have seen code in an `app.py` that looks something like:

if \_\_name\_\_ == '\_\_main\_\_':
    app.run()

However, this pattern is now considered less favorable than using the command line interface. So we'll be using the `flask` command in the terminal throughout.

Let's move on. What if we want to change our message to say "Hello Everyone!"? If we make a change in our `app.py`, we don't see it in the browser :( That is because our server is not watching for changes. To allow for that as well as more useful error messages when things go wrong, we need to enable debug mode when we're working on our project. To do that, we need to modify our terminal command:

FLASK\_APP=app.py FLASK\_DEBUG=1 flask run

When you start the server in this way, it will automatically detect changes and restart the server whenever you save file!

Now let's try to add another route to our application. When a user goes to `localhost:5000/name` we should return the text "Welcome to our application!". We will need to include another route as well as a function to run when that route is reached. Try this on your own first; if you are struggling, look at the solution below.

from flask import Flask

app = Flask(\_\_name\_\_)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/name')
def welcome():
    return "Welcome to our application!"

Great! We've seen how to build a very simple server with Flask, but we're just getting started. In the next section we will see how to make our routes a bit more dynamic and add parameters to our URLs.

### Shortening Our Terminal Command

It's possible to have our terminal set default values for `FLASK_APP` and `FLASK_DEBUG` so that we don't need to specify them every time you start the server.

In what follows, we'll talk about how to set sensible terminal defaults if you're using OSX. For tips if you're using Windows, check out the [Flask docs](http://flask.pocoo.org/docs/0.12/cli/).

On a Mac, one thing you can do is set the `FLASK_APP` and `FLASK_DEBUG` variables inside of the terminal session. In the terminal, you can type:

export FLASK_APP=app.py
export FLASK_DEBUG=1

Once these are set, you can type `flask run`, and as long as you've got a file called `app.py` with your Flask setup, you'll be good to go!

Unfortunately, if you close your terminal window, you'll lose those variables. The next time you open up terminal, you'll have to type those `export` statements again. If you want to set them once and forget about them, you can also put those two lines inside of your `.bashrc`, or, if you're using [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh), inside of your `.zshrc`.

As a reminder, to open up your `.zshrc`, you can type `code ~/.zshrc`, and add the two export lines above to the bottom of the file. After saving, to restart your terminal, you can then type `source ~/.zshrc`. After that, you can always type `flask run` to start your Flask server in debug mode! (If you're using `bash`, you can replace references to `.zhsrc` with `.bashrc`.)