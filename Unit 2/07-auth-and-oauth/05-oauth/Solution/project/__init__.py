# Flask and extensions
from flask import Flask, redirect, url_for
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_migrate import Migrate

# Create instance of Flask class
app = Flask(__name__)

# Configure Flask Modus
modus = Modus(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/users-oauth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure bcrypt
bcrypt = Bcrypt(app)

# Configure Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# Configure Flask Dance
twitter_blueprint = make_twitter_blueprint(
    api_key="WccILPLiPOw14vVm0QNUwEMtK",
    api_secret="XI296LpbPst9iRU7dgKFyiPLMZg25PBSpPJDywTSxqebX3BZI8",
)

# Configure Flask Migrate
migrate = Migrate(app, db)

# Set secret key
# For production set secret key in env variable: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "this_is_an_insecure_development_key"

# Import blueprints here to avoid circular imports
from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.tags.views import tags_blueprint

# Register blueprints
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(
    messages_blueprint, url_prefix='/users/<int:user_id>/messages')
app.register_blueprint(tags_blueprint, url_prefix='/tags')
# Register Flask Dance Twitter blueprint
app.register_blueprint(twitter_blueprint, url_prefix="/login")

# Finalize Flask Login setup

from project.users.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=["GET"])
def home():
    return redirect('users')

"""
@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])
"""
