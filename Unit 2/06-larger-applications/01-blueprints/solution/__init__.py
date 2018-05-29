# Flask and extensions
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_migrate import Migrate

# Create instance of Flask class
app = Flask(__name__)

# Configure Flask Modus
modus = Modus(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/users-messages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure WTForms
# For production set secret key in env variable: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "this_is_an_insecure_development_key"

# Import blueprints here to avoid circular imports
from solution.users.views import users_blueprint
from solution.messages.views import messages_blueprint

# Register blueprints
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(
    messages_blueprint, url_prefix='/users/<int:user_id>/messages')


@app.route('/', methods=["GET"])
def home():
    return redirect('users')
