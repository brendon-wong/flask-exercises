from flask import Flask, render_template, url_for, request, redirect

# Import ORM
from flask_sqlalchemy import SQLAlchemy

# Import Flask Modus
from flask_modus import Modus

# Create instance of Flask class, set custom template and static folder
app = Flask(__name__, template_folder="solution_templates",
            static_folder="solution_static")

# Configure Flask Modus
modus = Modus(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-sqlalchemy-snacks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# All models inherit from SQLAlchemy's db.Model
class Snack(db.Model):

    __tablename__ = "snacks"

    # Columns in table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    kind = db.Column(db.Text)

    # Row data
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    # Set a custom string representation of snack objects
    def __repr__(self):
        return f"{self.name} is a kind of {self.kind}"


@app.route('/', methods=["GET"])
def home():
    return redirect('snacks')


@app.route('/snacks', methods=["GET", "POST"])
def snacks():
    if request.method == "POST":
        new_snack = Snack(request.form["name"], request.form["kind"])
        db.session.add(new_snack)
        db.session.commit()
    return render_template('index.html', snacks=Snack.query.all())


@app.route('/snacks/new', methods=["GET"])
def new():
    return render_template('new.html')


@app.route('/snacks/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    selected_snack = Snack.query.get(id)
    # Use b"PATCH" because Flask Modus makes request.method a bytes literal
    if request.method == b"PATCH":
        selected_snack.name, selected_snack.kind = request.form['name'], request.form['kind']
        db.session.add(selected_snack)
        db.session.commit()
        return redirect(url_for('snacks'))
    if request.method == b"DELETE":
        db.session.delete(selected_snack)
        db.session.commit()
        return redirect(url_for('snacks'))
    return render_template('show.html', snack=selected_snack)


@app.route('/snacks/<int:id>/edit', methods=["GET"])
def edit(id):
    return render_template('edit.html', snack=Snack.query.get(id))


# Allows app to be run with python3 file_name.py
if __name__ == '__main__':
    # Enable development mode
    app.config['ENV'] = 'development'
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
