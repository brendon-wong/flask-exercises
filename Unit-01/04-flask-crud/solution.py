from flask import Flask, render_template, url_for, request, redirect

# Import Snack class representing application data
from solution_snack import Snack

# Import Flask Modus
from flask_modus import Modus

# Create instance of Flask class, set custom template and static folder
app = Flask(__name__, template_folder="solution_templates",
            static_folder="solution_static")
# Configure Flask Modus
modus = Modus(app)


# Empty snack_list to pass tests
snack_list = []

# Seed the app with snacks, does not work with tests
# lays = Snack("Lays", "Chips")
# doritos = Snack("Doritos", "Chips")
# cheetos = Snack("Cheetos", "Chips")
# apples = Snack("Apples", "Fruits")
# oranges = Snack("Oranges", "Fruits")
# almonds = Snack("Almonds", "Nuts")
# snack_list = [lays, doritos, cheetos, apples, oranges, almonds]


@app.route('/', methods=["GET"])
def home():
    return redirect('snacks')


@app.route('/snacks', methods=["GET", "POST"])
def snacks():
    if request.method == "POST":
        new_snack = Snack(request.form["name"], request.form["kind"])
        snack_list.append(new_snack)
    return render_template('index.html', snacks=snack_list)


@app.route('/snacks/new', methods=["GET"])
def new():
    return render_template('new.html')


@app.route('/snacks/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    # Create a generator and get first element with next
    selected_snack = next(snack for snack in snack_list if snack.id == id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        selected_snack.name = request.form['name']
        selected_snack.kind = request.form['kind']
        return redirect(url_for('snacks'))
    if request.method == b"DELETE":
        snack_list.remove(selected_snack)
        return redirect(url_for('snacks'))
    return render_template('show.html', snack=selected_snack)


@app.route('/snacks/<int:id>/edit', methods=["GET"])
def edit(id):
    # Create a generator and get first element with next
    selected_snack = next(snack for snack in snack_list if snack.id == id)
    return render_template('edit.html', snack=selected_snack)


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
