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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/bp-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure WTForms
# For production set secret key in env variable: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "this_is_an_insecure_development_key"

# Configure Flask Migrate
migrate = Migrate(app, db)

# Import blueprints here to avoid circular imports
from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.tags.views import tags_blueprint

# Register blueprints
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(
    messages_blueprint, url_prefix='/users/<int:user_id>/messages')
app.register_blueprint(tags_blueprint, url_prefix='/tags')


@app.route('/', methods=["GET"])
def home():
    return redirect('users')

