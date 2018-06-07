# Import a class named Flask from flask library
from flask import Flask

# Create instance of Flask class
app = Flask(__name__)


# listen for route /welcome
@app.route('/welcome')
def welcome():
    # Return statement contains response sent to the site visitor
    return "welcome"


# Listen for route /welcome/home
@app.route('/welcome/home')
def welcome_home():
    return "welcome home"


# Listen for route /welcome/back
@app.route('/welcome/back')
def welcome_back():
    return "welcome back"


# Listen for route /sum
@app.route('/sum')
def sum():
    sum = 5 + 5
    return str(sum)


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
