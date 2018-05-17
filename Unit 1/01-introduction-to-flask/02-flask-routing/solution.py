# Import a class named Flask from flask library
from flask import Flask

# Create instance of Flask class
app = Flask(__name__)


# Accept two numbers using the two path segments after add
@app.route('/add/<int:n1>/<int:n2>')
def add(n1, n2):
    # Add n1 and n2 and send the result to the site visitor
    return str(n1 + n2)


@app.route('/subtract/<int:n1>/<int:n2>')
def subtract(n1, n2):
    return str(n1 - n2)


@app.route('/multiply/<int:n1>/<int:n2>')
def multiply(n1, n2):
    return str(n1 * n2)


@app.route('/divide/<int:n1>/<int:n2>')
def divide(n1, n2):
    return str(n1 / n2)


@app.route('/math/<operation>/<int:n1>/<int:n2>')
def math(operation, n1, n2):
    if operation == "add":
        return str(n1 + n2)
    if operation == "subtract":
        return str(n1 - n2)
    if operation == "multiply":
        return str(n1 * n2)
    if operation == "divide":
        return str(n1 / n2)
    else:
        return "Operation not supported"


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
