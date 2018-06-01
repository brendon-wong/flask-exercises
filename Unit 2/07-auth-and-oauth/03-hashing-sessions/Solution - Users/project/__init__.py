# Flask and extensions
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Create instance of Flask class
app = Flask(__name__)

# Configure Flask Modus
modus = Modus(app)

# Configure bcrypt
bcrypt = Bcrypt(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Flask Migrate
migrate = Migrate(app, db)

# Set secret key for WTForms, sessions, etc
# For production set secret key in env variable: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "this_is_an_insecure_development_key"

from project.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')

@app.route('/', methods=["GET"])
def home():
    return redirect('users')