from flask import Flask, render_template, url_for, request, redirect

# Import CRUD functions
from solution_db import *

# Import Flask Modus
from flask_modus import Modus

# Create instance of Flask class, set custom template and static folder
app = Flask(__name__, template_folder="solution_templates",
            static_folder="solution_static")
# Configure Flask Modus
modus = Modus(app)

# Seed the app with snacks
# create_snack("Lays", "Chips")
# create_snack("Doritos", "Chips")
# create_snack("Cheetos", "Chips")
# create_snack("Apples", "Fruits")
# create_snack("Oranges", "Fruits")
# create_snack("Almonds", "Nuts")


@app.route('/', methods=["GET"])
def home():
    return redirect('snacks')


@app.route('/snacks', methods=["GET", "POST"])
def snacks():
    if request.method == "POST":
        new_snack = create_snack(request.form["name"], request.form["kind"])
    return render_template('index.html', snacks=find_all_snacks())


@app.route('/snacks/new', methods=["GET"])
def new():
    return render_template('new.html')


@app.route('/snacks/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        edit_snack(request.form['name'], request.form['kind'], id)
        return redirect(url_for('snacks'))
    if request.method == b"DELETE":
        remove_snack(id)
        return redirect(url_for('snacks'))
    selected_snack = find_snack(id)
    return render_template('show.html', snack=selected_snack)


@app.route('/snacks/<int:id>/edit', methods=["GET"])
def edit(id):
    selected_snack = find_snack(id)
    return render_template('edit.html', snack=selected_snack)


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
